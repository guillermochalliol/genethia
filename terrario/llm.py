"""LLM clients: OpenRouter (real) and a deterministic mock, behind one interface.

Walls enforced here:
- Every model must have a pinned provider with allow_fallbacks=false, or the client refuses to start.
- An in-process budget stops new calls once spent >= max_total_usd * stop_at_fraction.
  Calls already in flight still finish, so the overshoot is bounded by `concurrency` calls.
- The provider that served each call is recorded from the response, and `audit_providers`
  re-checks it later against /generation (that endpoint lags ~10-15 s behind a completion,
  so blocking on it per call would add that delay to every round).
- The API key is read from OPENROUTER_API_KEY and never stored in results or logs.

Clients only return text plus metadata. Logging is the orchestrator's job (`LLMResult.to_log`).
"""

from __future__ import annotations

import asyncio
import contextvars
import hashlib
import json
import os
import random
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

import httpx

from .actions import ComprehensionAnswer, Phase0Action, Phase1Action, Phase2Action, RatificationVote

Message = dict[str, str]

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}

# Set by the orchestrator for each run. Only the mock reads it: identical prompts in different
# runs (e.g. the post-run questions) must still give run-specific simulated answers.
RUN_KEY: contextvars.ContextVar[str] = contextvars.ContextVar("RUN_KEY", default="")


class LLMError(RuntimeError):
    """A call failed for good (non-retryable status or retries exhausted)."""


class BudgetExhausted(RuntimeError):
    """The in-process spending cap was reached; no new calls are allowed."""


class ConfigError(ValueError):
    pass


@dataclass
class LLMResult:
    model: str
    text: str
    finish_reason: str | None
    generation_id: str | None
    provider: str | None  # provider that served the call, None if unknown
    provider_source: str  # "generation_api", "response_field", "mock" or "unknown"
    provider_ok: bool  # provider is one of the pinned ones
    prompt_tokens: int
    completion_tokens: int
    cached_tokens: int
    reasoning_tokens: int  # must stay 0 for models whose thinking is turned off
    cost_usd: float
    latency_s: float
    attempts: int
    mock: bool = False
    raw_usage: dict[str, Any] = field(default_factory=dict)

    def to_log(self) -> dict[str, Any]:
        return asdict(self)


class Budget:
    """Spending guard. Single event loop, so no lock is needed."""

    def __init__(self, max_total_usd: float, stop_at_fraction: float = 0.8):
        if max_total_usd <= 0 or not 0 < stop_at_fraction <= 1:
            raise ConfigError("budget needs max_total_usd > 0 and 0 < stop_at_fraction <= 1")
        self.max_total_usd = max_total_usd
        self.limit_usd = max_total_usd * stop_at_fraction
        self.spent_usd = 0.0
        self.calls = 0

    @property
    def exhausted(self) -> bool:
        return self.spent_usd >= self.limit_usd

    def check(self) -> None:
        if self.exhausted:
            raise BudgetExhausted(
                f"spent {self.spent_usd:.4f} USD >= stop limit {self.limit_usd:.4f} USD"
            )

    def add(self, cost_usd: float) -> None:
        self.spent_usd += cost_usd
        self.calls += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "spent_usd": round(self.spent_usd, 6),
            "limit_usd": self.limit_usd,
            "max_total_usd": self.max_total_usd,
            "calls": self.calls,
        }


class LLMClient(Protocol):
    budget: Budget

    async def complete(self, model: str, messages: list[Message]) -> LLMResult: ...

    async def aclose(self) -> None: ...


def _validate_pins(models: set[str], provider_by_model: dict[str, dict[str, Any]]) -> None:
    for m in sorted(models):
        pin = provider_by_model.get(m)
        if not pin or not (pin.get("order") or pin.get("only")):
            raise ConfigError(f"model {m!r} has no pinned provider (order/only)")
        if pin.get("allow_fallbacks") is not False:
            raise ConfigError(f"model {m!r} must set allow_fallbacks: false")


def _pinned_names(pin: dict[str, Any]) -> set[str]:
    return {p.lower() for p in (pin.get("only") or pin.get("order") or [])}


class OpenRouterClient:
    def __init__(
        self,
        llm_cfg: dict[str, Any],
        budget: Budget,
        models: set[str],
        api_key: str | None = None,
        verify_provider: bool = False,
        transport: httpx.AsyncBaseTransport | None = None,
        sleep=asyncio.sleep,
    ):
        self.cfg = llm_cfg
        self.budget = budget
        self.pins: dict[str, dict[str, Any]] = llm_cfg.get("provider_by_model", {})
        # Per-model request fields, e.g. {"reasoning": {"effort": "none"}} to turn thinking off.
        self.extra: dict[str, dict[str, Any]] = llm_cfg.get("request_extra_by_model", {})
        _validate_pins(models, self.pins)
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise ConfigError("OPENROUTER_API_KEY is not set (use --mock to test without it)")
        self.verify_provider = verify_provider
        self.max_retries = int(llm_cfg.get("max_retries", 2))
        # 429s are upstream rate limits, not bad outputs: they get their own, longer budget.
        self.rate_limit_retries = int(llm_cfg.get("rate_limit_retries", 6))
        self._sem = asyncio.Semaphore(int(llm_cfg.get("concurrency", 6)))
        self._sleep = sleep
        self._http = httpx.AsyncClient(
            base_url=llm_cfg["base_url"].rstrip("/") + "/",
            headers={"Authorization": f"Bearer {key}", "X-Title": "Genethia terrario"},
            timeout=float(llm_cfg.get("timeout_seconds", 60)),
            transport=transport,
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    def _body(self, model: str, messages: list[Message]) -> dict[str, Any]:
        provider = {"require_parameters": True, **self.pins[model], "allow_fallbacks": False}
        return {
            "model": model,
            "messages": messages,
            "temperature": self.cfg.get("temperature", 0.7),
            "max_tokens": self.cfg.get("max_tokens", 350),
            **self.extra.get(model, {}),
            "provider": provider,
        }

    async def _backoff(self, attempt: int, retry_after: str | None) -> None:
        delay = min(2.0**attempt, 20.0) + random.uniform(0, 0.5)
        if retry_after:
            try:
                delay = max(delay, min(float(retry_after), 60.0))
            except ValueError:
                pass
        await self._sleep(delay)

    async def _post(self, body: dict[str, Any]) -> httpx.Response:
        """POST, waiting out 429s (backoff up to 20 s, or Retry-After) before giving up."""
        for k in range(self.rate_limit_retries + 1):
            r = await self._http.post("chat/completions", json=body)
            if r.status_code != 429 or k == self.rate_limit_retries:
                return r
            await self._backoff(k + 1, r.headers.get("retry-after"))
        raise AssertionError("unreachable")

    async def complete(self, model: str, messages: list[Message]) -> LLMResult:
        if model not in self.pins:
            raise ConfigError(f"model {model!r} has no pinned provider")
        async with self._sem:
            # Check after acquiring the slot, so queued calls see the latest spend.
            self.budget.check()
            body = self._body(model, messages)
            t0 = time.monotonic()
            last_err = "unknown"
            for attempt in range(self.max_retries + 1):
                try:
                    r = await self._post(body)
                except (httpx.TimeoutException, httpx.TransportError) as e:
                    last_err = f"{type(e).__name__}: {e}"
                    if attempt < self.max_retries:
                        await self._backoff(attempt, None)
                        continue
                    break
                if r.status_code in RETRYABLE_STATUS:
                    last_err = f"HTTP {r.status_code}: {r.text[:300]}"
                    if attempt < self.max_retries:
                        await self._backoff(attempt, r.headers.get("retry-after"))
                        continue
                    break
                if r.status_code != 200:
                    # 400/401/402/403/404: retrying will not help. 402 means no credits left.
                    raise LLMError(f"{model}: HTTP {r.status_code}: {r.text[:300]}")
                data = r.json()
                choice = (data.get("choices") or [{}])[0]
                if "error" in data or choice.get("error") or choice.get("finish_reason") == "error":
                    err = data.get("error") or choice.get("error") or {}
                    last_err = f"in-body error: {json.dumps(err)[:300]}"
                    # A failed generation may still be billed.
                    self.budget.add(float((data.get("usage") or {}).get("cost") or 0.0))
                    if attempt < self.max_retries:
                        await self._backoff(attempt, None)
                        continue
                    break
                return await self._result(model, data, choice, time.monotonic() - t0, attempt + 1)
            raise LLMError(f"{model}: gave up after {self.max_retries + 1} attempts: {last_err}")

    async def _result(
        self, model: str, data: dict, choice: dict, latency: float, attempts: int
    ) -> LLMResult:
        usage = data.get("usage") or {}
        gen_id = data.get("id")
        cost = usage.get("cost")
        provider, source = data.get("provider"), "response_field" if data.get("provider") else "unknown"
        if self.verify_provider and gen_id:
            gen = await self._generation(gen_id)
            if gen:
                if gen.get("provider_name"):
                    provider, source = gen["provider_name"], "generation_api"
                if cost is None and gen.get("total_cost") is not None:
                    cost = gen["total_cost"]
        if cost is None:
            # Without a cost we cannot enforce the budget: stop rather than guess.
            raise LLMError(f"{model}: response {gen_id} has no cost; refusing to continue")
        self.budget.add(float(cost))
        details = usage.get("prompt_tokens_details") or {}
        out_details = usage.get("completion_tokens_details") or {}
        return LLMResult(
            model=model,
            text=(choice.get("message") or {}).get("content") or "",
            finish_reason=choice.get("finish_reason"),
            generation_id=gen_id,
            provider=provider,
            provider_source=source,
            provider_ok=bool(provider) and provider.lower() in _pinned_names(self.pins[model]),
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
            cached_tokens=int(details.get("cached_tokens") or 0),
            reasoning_tokens=int(out_details.get("reasoning_tokens") or 0),
            cost_usd=float(cost),
            latency_s=round(latency, 3),
            attempts=attempts,
            raw_usage=usage,
        )

    async def audit_providers(self, calls: list[tuple[str, str]]) -> list[dict[str, Any]]:
        """For (generation_id, model) pairs, ask /generation who served each call."""

        async def one(gen_id: str, model: str) -> dict[str, Any]:
            async with self._sem:
                gen = await self._generation(gen_id, delays=(2.0, 4.0, 8.0, 16.0, 30.0, 30.0, 30.0))
            name = (gen or {}).get("provider_name")
            return {
                "generation_id": gen_id, "model": model, "provider_name": name,
                "total_cost": (gen or {}).get("total_cost"),
                "ok": bool(name) and name.lower() in _pinned_names(self.pins[model]),
            }

        return list(await asyncio.gather(*[one(g, m) for g, m in calls]))

    async def _generation(
        self, gen_id: str, delays: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0)
    ) -> dict[str, Any] | None:
        """Fetch generation metadata; it lags behind the completion, so retry 404s."""
        for delay in delays:
            try:
                r = await self._http.get("generation", params={"id": gen_id})
            except (httpx.TimeoutException, httpx.TransportError):
                r = None
            if r is not None and r.status_code == 200:
                return r.json().get("data") or {}
            if r is not None and r.status_code not in (404, *RETRYABLE_STATUS):
                return None
            await self._sleep(delay)
        return None


# --------------------------------------------------------------------------- mock


@dataclass
class MockBehavior:
    """Probabilities for the simulated agents. Defaults aim to exercise every code path."""

    p_invalid: float = 0.08  # unparseable or schema-breaking output
    p_read_archive: float = 0.25
    p_copy_given_read: float = 0.6
    p_misreport: float = 0.2  # announces fewer fish than taken
    p_tell_village: float = 0.3
    take_weights: tuple[float, ...] = (0.05, 0.15, 0.3, 0.25, 0.15, 0.1)  # for 0..5 fish
    usd_per_mtok_in: float = 0.05
    usd_per_mtok_out: float = 0.10
    latency_s: float = 0.0


_LOG_LINE = re.compile(r"^\s*(\S+): verified result = (-?\d+)\s*$", re.MULTILINE)
_NUMBER = re.compile(r"-?\d+")
_PHASE2_KEYS = set(Phase2Action.model_fields) - set(Phase1Action.model_fields)
_PHASE0_KEYS = set(Phase0Action.model_fields) - set(Phase1Action.model_fields)
_RATIFY_KEYS = set(RatificationVote.model_fields) - {"reasoning"}


class MockClient:
    """Deterministic fake: same (seed, model, messages) gives the same output, in any call order.

    It knows nothing about the true answers except what the prompt shows it, so it can only
    "cheat" by copying from the season log text, exactly like a real agent would.
    Prompts must name the schema fields (e.g. "final_answer") so the mock can tell the phase.
    """

    def __init__(
        self,
        budget: Budget,
        seed: int = 0,
        behavior: MockBehavior | None = None,
        models: set[str] | None = None,
        llm_cfg: dict[str, Any] | None = None,
    ):
        if models is not None and llm_cfg is not None:
            # Same wall as the real client, so a bad config fails in --mock too.
            _validate_pins(models, llm_cfg.get("provider_by_model", {}))
        self.budget = budget
        self.seed = seed
        self.b = behavior or MockBehavior()

    async def aclose(self) -> None:
        pass

    def _rng(self, model: str, messages: list[Message]) -> random.Random:
        h = hashlib.sha256(
            json.dumps([self.seed, RUN_KEY.get(), model, messages], sort_keys=True).encode()
        ).digest()
        return random.Random(int.from_bytes(h[:8], "big"))

    async def complete(self, model: str, messages: list[Message]) -> LLMResult:
        self.budget.check()
        rng = self._rng(model, messages)
        if self.b.latency_s:
            await asyncio.sleep(self.b.latency_s * rng.uniform(0.5, 1.5))
        prompt = "\n".join(m.get("content", "") for m in messages)
        last = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), prompt)
        if '"allowed_to_use"' in last:
            answer = {
                "log_contents": rng.choice(["Verified answers to this round's puzzles.", "Old records.",
                                            "I don't know."]),
                "allowed_to_use": rng.choice(["yes", "no", "unsure"])}
            if '"norms"' in last:
                answer["norms"] = rng.choice([
                    "We must announce truthfully what we took and not take more than our share.",
                    "Announce honestly; never take more than your fair share.",
                    "Nothing special.", "We should be kind to each other."])
            text = self._wrap(rng, answer)
        elif any(f'"{k}"' in last for k in _RATIFY_KEYS):
            text = self._wrap(rng, {"reasoning": "Sounds fair.", "adopt": rng.random() < 0.85})
        elif any(k in last for k in _PHASE2_KEYS):
            text = self._phase2(rng, prompt)
        elif any(k in last for k in _PHASE0_KEYS):
            text = self._phase0(rng)
        else:
            text = self._phase1(rng, prompt)
        p_tok, c_tok = max(1, len(prompt) // 4), max(1, len(text) // 4)
        cost = (p_tok * self.b.usd_per_mtok_in + c_tok * self.b.usd_per_mtok_out) / 1e6
        self.budget.add(cost)
        return LLMResult(
            model=model, text=text, finish_reason="stop",
            generation_id=f"mock-{rng.getrandbits(48):012x}",
            provider="mock", provider_source="mock", provider_ok=True,
            prompt_tokens=p_tok, completion_tokens=c_tok, cached_tokens=0, reasoning_tokens=0,
            cost_usd=cost, latency_s=0.0, attempts=1, mock=True,
        )

    def _invalid(self, rng: random.Random) -> str | None:
        if rng.random() >= self.b.p_invalid:
            return None
        return rng.choice([
            "I think the answer is probably around a hundred fish.",
            '{"reasoning": "count", "answer": "many", "read_archive": false}',
            '```json\n{"reasoning": "ok", "answer": 12, "fish_take": 9,\n```',
        ])

    def _own_guess(self, rng: random.Random, prompt: str) -> int:
        nums = [int(n) for n in _NUMBER.findall(prompt)] or [0]
        return rng.choice(nums) * rng.randint(2, 9) + rng.randint(-40, 40)

    def _phase1(self, rng: random.Random, prompt: str) -> str:
        if (bad := self._invalid(rng)) is not None:
            return bad
        take = rng.choices(range(len(self.b.take_weights)), weights=self.b.take_weights)[0]
        announce = take - rng.randint(1, take) if take and rng.random() < self.b.p_misreport else take
        action = {
            "reasoning": "I estimate the puzzle and keep the lake in mind.",
            # The mock cannot solve puzzles: own answers are plausible guesses, almost always
            # wrong. A correct answer in the mock means the agent copied from the season log.
            "answer": self._own_guess(rng, prompt),
            "read_archive": rng.random() < self.b.p_read_archive,
            "fish_take": take,
            "fish_announce": announce,
            "message": rng.choice(["", "Let us keep the lake healthy.", "I took a fair share."]),
        }
        return self._wrap(rng, action)

    def _phase0(self, rng: random.Random) -> str:
        if (bad := self._invalid(rng)) is not None:
            return bad
        return self._wrap(rng, {"reasoning": "Deciding where to go.",
                                "visit_archive": rng.random() < self.b.p_read_archive})

    def _phase2(self, rng: random.Random, prompt: str) -> str:
        if (bad := self._invalid(rng)) is not None:
            return bad
        logged = dict(_LOG_LINE.findall(prompt))
        # Own task id: one that appears in the prompt outside the log lines.
        outside = _LOG_LINE.sub("", prompt)
        mine = next((tid for tid in logged if tid in outside), None)
        copy = mine is not None and rng.random() < self.b.p_copy_given_read
        final = int(logged[mine]) if copy else self._own_guess(rng, outside)
        action = {
            "reasoning": "The archive page looks relevant." if copy else "I keep my own work.",
            "final_answer": final,
            "tell_village": rng.random() < self.b.p_tell_village,
        }
        return self._wrap(rng, action)

    @staticmethod
    def _wrap(rng: random.Random, action: dict[str, Any]) -> str:
        body = json.dumps(action)
        style = rng.randrange(3)
        if style == 0:
            return body
        if style == 1:
            return f"```json\n{body}\n```"
        return f"Here is my decision.\n{body}"


def make_client(
    config: dict[str, Any], mock: bool, seed: int = 0, parallel_runs: int = 1
) -> LLMClient:
    """Build one client (one budget) for all runs. Budget comes from config["budget"].

    With several villages at once, the call semaphore grows to concurrency * parallel_runs,
    so every village can still send its agents' calls in parallel.
    """
    budget = Budget(**config["budget"])
    models = {m["model"] for m in config["village"]["members"]}
    if mock:
        return MockClient(budget, seed=seed, models=models, llm_cfg=config["llm"])
    llm = {**config["llm"], "concurrency": int(config["llm"].get("concurrency", 6)) * parallel_runs}
    return OpenRouterClient(llm, budget, models)
