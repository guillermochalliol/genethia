"""Round-based orchestrator for the pilot. The only component that acts on the world.

One run = one condition x one seed, with its own hash-chained log. Agents only produce
text; this module parses it with Pydantic (never exec/eval), applies it and logs everything.
The log records facts (truths, actions, takes, scores); metrics are derived later from it.
"""

from __future__ import annotations

import asyncio
import hashlib
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from . import prompts
from .actions import (
    ComprehensionAnswer, Phase0Action, Phase1Action, Phase1StepAction, Phase2Action,
    RatificationVote, parse_action,
)
from .conditions import CONDITIONS, RATIFIED
from .eventlog import EventLog
from .llm import BudgetExhausted, LLMClient, LLMError, Message, MockClient
from .world import Puzzle, WorldState, make_puzzle, season_log_text


@dataclass
class Agent:
    agent_id: str
    model: str
    points: int = 0
    history: list[Message] = field(default_factory=list)


class Orchestrator:
    def __init__(
        self, config: dict[str, Any], condition: str, seed: int, rounds: int,
        client: LLMClient, run_dir: Path,
    ):
        self.cfg = config
        self.world_cfg = config["world"]
        self.condition = condition
        self.condition_text = CONDITIONS[condition]
        self.seed = seed
        self.rounds = rounds
        self.client = client
        self.max_retries = int(config["llm"].get("max_retries", 2))
        self.log = EventLog(run_dir / "events.jsonl")
        # Same seed gives the same puzzles and serving order in every condition (paired design).
        self.puzzle_rng = random.Random(f"{seed}-puzzles")
        self.order_rng = random.Random(f"{seed}-order")
        self.agents = [
            Agent(f"A{i + 1}", m["model"]) for i, m in enumerate(config["village"]["members"])
        ]
        self.world = WorldState(
            stock=float(self.world_cfg["stock_start"]),
            cap=float(self.world_cfg["stock_cap"]),
            regrowth=float(self.world_cfg["regrowth_rate"]),
            max_take=int(self.world_cfg["max_take_per_round"]),
        )
        self.public_board: list[dict[str, Any]] = []
        self._budget_hit = False
        # World rules set by calibration knobs (identical in every condition).
        self.quota_on = bool(self.world_cfg.get("announce_quota", False))
        self.feedback_on = bool(self.world_cfg.get("answer_feedback", False))
        self.archive_step = bool(self.world_cfg.get("archive_step", False))
        self.notice = self.world_cfg.get("plaza_notice")
        n = len(self.agents)
        self.quota = prompts.fair_quota(self.world_cfg, n)
        self.restricted_take = prompts.restricted_max_take(self.world_cfg, n)
        self.access = {a.agent_id: self.world.max_take for a in self.agents}
        self.feedback: dict[str, dict[str, Any]] = {}
        self._served: list[tuple[str, str]] = []  # (generation_id, model) for the audit

    # ------------------------------------------------------------------ calls

    async def _act(
        self, agent: Agent, round_no: int, phase: int | str, messages: list[Message],
        schema: type[BaseModel], schema_text: str,
    ) -> tuple[BaseModel | None, list[Message]]:
        """Call the model, validate, retry on invalid output. Returns (action or None, messages)."""
        msgs = list(messages)
        for attempt in range(self.max_retries + 1):
            try:
                res = await self.client.complete(agent.model, msgs)
            except BudgetExhausted:
                # Let sibling calls finish cleanly; the round is aborted after the gather.
                self._budget_hit = True
                return None, msgs
            except LLMError as e:
                self.log.append("llm_error", round=round_no, agent=agent.agent_id,
                                model=agent.model, phase=phase, attempt=attempt, error=str(e))
                return None, msgs
            if res.generation_id and not res.mock:
                self._served.append((res.generation_id, agent.model))
            action, err = parse_action(res.text, schema)
            self.log.append(
                "llm_call", round=round_no, agent=agent.agent_id, phase=phase, attempt=attempt,
                prompt_sha256=hashlib.sha256(repr(msgs).encode()).hexdigest(),
                prompt_last=msgs[-1]["content"], response=res.text, valid=action is not None,
                parse_error=err, **{k: v for k, v in res.to_log().items() if k != "text"},
            )
            msgs = msgs + [{"role": "assistant", "content": res.text}]
            if action is not None:
                return action, msgs
            msgs = msgs + [{"role": "user", "content": prompts.retry_user(err or "?", schema_text)}]
        return None, msgs

    # ------------------------------------------------------------------ round

    async def _round(self, round_no: int) -> None:
        stock_before = int(self.world.stock)
        self.log.append("round_start", round=round_no, stock=stock_before,
                        collapsed=self.world.collapsed, budget=self.client.budget.snapshot())
        puzzles: dict[str, Puzzle] = {
            a.agent_id: make_puzzle(self.puzzle_rng, f"R{round_no:02d}-{a.agent_id}",
                                    self.world_cfg.get("puzzle_difficulty", "medium"))
            for a in self.agents
        }
        if self.quota_on:
            self.log.append("access", round=round_no, quota=self.quota, max_take=self.access)
        for aid, p in puzzles.items():
            self.log.append("puzzle", round=round_no, agent=aid, task_id=p.task_id,
                            text=p.text, truth=p.answer)

        n = len(self.agents)

        def context(a: Agent) -> str:
            return prompts.round_context(
                round_no, self.rounds, stock_before, a.points, puzzles[a.agent_id],
                self.public_board, bool(self.world_cfg.get("archive_mention", False)),
                max_take=self.access[a.agent_id] if self.quota_on else None,
                restricted=self.access[a.agent_id] < self.world.max_take,
                feedback=self.feedback.get(a.agent_id) if self.feedback_on else None,
                notice=self.notice)

        def system(a: Agent) -> Message:
            return {"role": "system", "content": prompts.system_prompt(
                a.agent_id, n, self.condition_text, self.world_cfg)}

        visiting: dict[str, bool] = {}
        if self.archive_step:
            # Phase 0: a separate yes/no archive decision before answering.
            p0 = await asyncio.gather(*[
                self._act(a, round_no, 0,
                          [system(a), {"role": "user", "content": prompts.phase0_user(context(a))}],
                          Phase0Action, prompts.PHASE0_SCHEMA)
                for a in self.agents
            ])
            self._abort_if_budget_hit(round_no)
            p0_msgs: dict[str, list[Message]] = {}
            for a, (act, msgs) in zip(self.agents, p0):
                visiting[a.agent_id] = bool(act and act.visit_archive)
                p0_msgs[a.agent_id] = msgs
                self.log.append("action", round=round_no, agent=a.agent_id, model=a.model, phase=0,
                                abstained=act is None, **(act.model_dump() if act else {}))
            p1_calls = [
                self._act(a, round_no, 1, p0_msgs[a.agent_id] + [{
                    "role": "user", "content": prompts.phase1_step_user(visiting[a.agent_id], puzzles[a.agent_id])}],
                    Phase1StepAction, prompts.PHASE1_STEP_SCHEMA)
                for a in self.agents
            ]
        else:
            p1_calls = [
                self._act(a, round_no, 1,
                          [system(a), {"role": "user", "content": prompts.phase1_user(context(a))}],
                          Phase1Action, prompts.PHASE1_SCHEMA)
                for a in self.agents
            ]

        # Phase 1: everyone in parallel, without seeing each other's choices.
        p1 = await asyncio.gather(*p1_calls)
        self._abort_if_budget_hit(round_no)
        if self.archive_step:
            for a, (act, _) in zip(self.agents, p1):
                if act is not None:
                    act.read_archive = visiting[a.agent_id]
        p1_actions: dict[str, Phase1Action | None] = {}
        p1_msgs: dict[str, list[Message]] = {}
        for a, (act, msgs) in zip(self.agents, p1):
            p1_actions[a.agent_id], p1_msgs[a.agent_id] = act, msgs  # type: ignore[assignment]
            self.log.append(
                "action", round=round_no, agent=a.agent_id, model=a.model, phase=1,
                abstained=act is None, **(act.model_dump() if act else {}),
            )

        # Phase 2: only for those who chose to read the archive.
        archive = season_log_text(puzzles)
        readers = [a for a in self.agents if (act := p1_actions[a.agent_id]) and act.read_archive]
        for a in readers:
            self.log.append("archive_read", round=round_no, agent=a.agent_id,
                            shown_task_ids=list(p.task_id for p in puzzles.values()))
        p2 = await asyncio.gather(*[
            self._act(
                a, round_no, 2,
                p1_msgs[a.agent_id] + [{"role": "user", "content": prompts.phase2_user(
                    puzzles[a.agent_id], p1_actions[a.agent_id].answer, archive)}],
                Phase2Action, prompts.PHASE2_SCHEMA,
            )
            for a in readers
        ])
        self._abort_if_budget_hit(round_no)
        p2_actions: dict[str, Phase2Action | None] = {}
        for a, (act, _) in zip(readers, p2):
            p2_actions[a.agent_id] = act  # type: ignore[assignment]
            self.log.append("action", round=round_no, agent=a.agent_id, model=a.model, phase=2,
                            abstained=act is None, **(act.model_dump() if act else {}))

        # Apply: fish first (random serving order), then score answers.
        raw = {aid: (act.fish_take if act else 0) for aid, act in p1_actions.items()}
        # Requests above the agent's access limit are clipped; the agent was told its limit.
        requested = {aid: min(v, self.access[aid]) for aid, v in raw.items()}
        actual = self.world.apply_takes(requested, self.order_rng)
        self.log.append("fish", round=round_no, stock_before=stock_before, requested_raw=raw,
                        requested=requested, actual=actual, stock_after=self.world.stock)
        board = []
        for a in self.agents:
            act1 = p1_actions[a.agent_id]
            act2 = p2_actions.get(a.agent_id)
            own = act1.answer if act1 else None
            # Phase 2 abstention keeps the phase-1 answer.
            final = act2.final_answer if act2 else own
            truth = puzzles[a.agent_id].answer
            correct = final is not None and final == truth
            gained = (self.world_cfg["points_per_correct_answer"] if correct else 0) + \
                actual[a.agent_id] * self.world_cfg["points_per_fish"]
            a.points += gained
            self.feedback[a.agent_id] = {"task_id": puzzles[a.agent_id].task_id,
                                         "correct": correct, "truth": truth}
            self.log.append(
                "score", round=round_no, agent=a.agent_id, own_answer=own, final_answer=final,
                truth=truth, correct=correct, fish_requested=requested[a.agent_id],
                fish_requested_raw=raw[a.agent_id],
                fish_actual=actual[a.agent_id],
                fish_announced=act1.fish_announce if act1 else None,
                points_gained=gained, points_total=a.points,
            )
            board.append({"agent": a.agent_id,
                          "announced": act1.fish_announce if act1 else None,
                          "message": act1.message if act1 else "",
                          "told_archive": bool(act2 and act2.tell_village)})
        self.public_board = board
        for a in self.agents:
            act1 = p1_actions[a.agent_id]
            over = self.quota_on and act1 is not None and act1.fish_announce > self.quota
            self.access[a.agent_id] = self.restricted_take if over else self.world.max_take
        self.log.append("public_board", round=round_no, board=board)

        self.world.regrow()
        self.log.append("round_end", round=round_no, stock=self.world.stock,
                        collapsed=self.world.collapsed,
                        points={a.agent_id: a.points for a in self.agents})

    async def _ratify(self) -> None:
        """C only, before round 1: every agent votes on the proposed commitments (round 0)."""
        n = len(self.agents)
        votes = await asyncio.gather(*[
            self._act(a, 0, "ratification",
                      prompts.ratification_messages(a.agent_id, n, self.condition_text, self.world_cfg),
                      RatificationVote, prompts.RATIFY_SCHEMA)
            for a in self.agents
        ])
        self._abort_if_budget_hit(0)
        yes = 0
        for a, (act, _) in zip(self.agents, votes):
            self.log.append("ratification_vote", round=0, agent=a.agent_id, model=a.model,
                            abstained=act is None, **(act.model_dump() if act else {}))
            yes += bool(act and act.adopt)
        # Pre-specified: the commitments stay in force whatever the result; the vote is reported.
        self.log.append("ratification_result", round=0, yes=yes, n=n, adopted_by_majority=yes > n / 2)

    async def _comprehension(self) -> None:
        """After the last round of a completed run: two questions per agent (secondary, logged)."""
        post = self.rounds + 1  # outside the played rounds, so round metrics never include it
        n = len(self.agents)
        answers = await asyncio.gather(*[
            self._act(a, post, "comprehension",
                      [{"role": "system", "content": prompts.system_prompt(
                          a.agent_id, n, self.condition_text, self.world_cfg)},
                       {"role": "user", "content": prompts.comprehension_user()}],
                      ComprehensionAnswer, prompts.COMPREHENSION_SCHEMA)
            for a in self.agents
        ])
        for a, (act, _) in zip(self.agents, answers):
            self.log.append("comprehension_answer", round=post, agent=a.agent_id, model=a.model,
                            abstained=act is None, **(act.model_dump() if act else {}))

    def _abort_if_budget_hit(self, round_no: int) -> None:
        if self._budget_hit:
            # Nothing of this round is applied; metrics only count rounds with a round_end.
            self.log.append("round_aborted", round=round_no, reason="budget_exhausted")
            raise BudgetExhausted(f"budget reached during round {round_no}")

    async def run(self) -> str:
        self.log.append(
            "run_start", condition=self.condition, seed=self.seed, rounds=self.rounds,
            condition_sha256=hashlib.sha256(self.condition_text.encode()).hexdigest(),
            members=[{"agent": a.agent_id, "model": a.model} for a in self.agents],
            world=self.world_cfg, llm={k: v for k, v in self.cfg["llm"].items()},
            mock=isinstance(self.client, MockClient),
        )
        reason = "completed"
        try:
            if self.condition in RATIFIED:
                await self._ratify()
            for r in range(1, self.rounds + 1):
                await self._round(r)
            # Only after the last round, never before: the questions must not affect play.
            await self._comprehension()
        except BudgetExhausted as e:
            reason = f"budget_exhausted: {e}"
        if self._served and hasattr(self.client, "audit_providers"):
            audit = await self.client.audit_providers(self._served)
            self.log.append(
                "provider_audit", calls=audit,
                verified=sum(1 for a in audit if a["provider_name"]),
                mismatches=[a for a in audit if a["provider_name"] and not a["ok"]],
                unverified=[a["generation_id"] for a in audit if not a["provider_name"]],
            )
        self.log.append("run_end", reason=reason, budget=self.client.budget.snapshot())
        return reason
