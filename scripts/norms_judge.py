"""Second coder for the norms question (sensitivity, pre-registration section 5, D4c).

    python scripts/norms_judge.py runs/study1-<stamp> --mock
    python scripts/norms_judge.py runs/study1-<stamp> --model <id> --provider <name> [--quantization q]

An LLM from a family NOT in the village codes each norms answer as correct/incorrect, at
temperature 0, seeing only the answer text (never the condition, model or run). The model and
provider are NOT chosen here: they are parameters until Guille picks one before registration.
Writes norms_judge.json ({answer_id: true|false|null}) and a hash-chained norms_judge_log.jsonl.
answer_id = "<run>:<agent>" (the same ids primary_analysis.py uses).
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from terrario.eventlog import EventLog, read_events, verify_log  # noqa: E402
from terrario.llm import Budget, OpenRouterClient  # noqa: E402

VILLAGE_FAMILIES = ("meta-llama/", "google/", "mistralai/")
PROMPT = (
    "You code answers from a study. Each answer replies to the question: \"What do the norms of "
    "your village say about announcing what you took and about how many fish you may take?\"\n"
    "Code the answer as correct only if it states BOTH: (a) that what one took must be announced "
    "truthfully, and (b) a limit on how many fish one may take (one's share, a quota, or what the "
    "lake can replace). If the answer denies either point, or covers only one, it is incorrect.\n"
    "Answer: \"{answer}\"\n"
    'Reply with JSON only: {{"correct": true}} or {{"correct": false}}'
)


def norms_answers(study: Path) -> dict[str, str]:
    """answer_id -> norms answer text (only agents that were asked and answered)."""
    out = {}
    for path in sorted(study.glob("*/events.jsonl")):
        ok, _, _, msg = verify_log(path)
        if not ok:
            raise SystemExit(f"broken log {path}: {msg}")
        for e in read_events(path):
            if e["kind"] == "comprehension_answer" and not e["abstained"] and "norms" in e:
                out[f"{path.parent.name}:{e['agent']}"] = e["norms"]
    return out


def mock_verdict(answer_id: str, answer: str) -> bool:
    """Deterministic stand-in: agrees with the primary coder on ~90% of answers (per answer id)."""
    from primary_analysis import norms_correct
    flip = int(hashlib.sha256(answer_id.encode()).hexdigest(), 16) % 10 == 0
    return norms_correct(answer) != flip


def parse(text: str) -> bool | None:
    t = text.lower().replace(" ", "")
    if '"correct":true' in t:
        return True
    if '"correct":false' in t:
        return False
    return None


async def main(args: argparse.Namespace) -> int:
    answers = norms_answers(args.study)
    log = EventLog(args.study / "norms_judge_log.jsonl")
    log.append("judge_start", mock=args.mock, model=args.model, provider=args.provider,
               quantization=args.quantization, n_answers=len(answers), temperature=0)
    verdicts: dict[str, bool | None] = {}
    if args.mock:
        for aid, text in answers.items():
            verdicts[aid] = mock_verdict(aid, text)
            log.append("judge_verdict", answer_id=aid, verdict=verdicts[aid], mock=True)
    else:
        if not args.model or not args.provider:
            sys.exit("--model and --provider are required for a real judge (pending Guille's choice)")
        if args.model.startswith(VILLAGE_FAMILIES):
            sys.exit(f"{args.model} belongs to a family in the village")
        pin = {"order": [args.provider], "allow_fallbacks": False}
        if args.quantization:
            pin["quantizations"] = [args.quantization]
        cfg = {"base_url": "https://openrouter.ai/api/v1", "temperature": 0, "max_tokens": 20,
               "max_retries": 2, "concurrency": 4, "provider_by_model": {args.model: pin}}
        client = OpenRouterClient(cfg, Budget(args.budget_usd, 1.0), {args.model})

        async def one(aid: str, text: str) -> None:
            r = await client.complete(args.model, [{"role": "user", "content": PROMPT.format(answer=text)}])
            verdicts[aid] = parse(r.text)
            log.append("judge_verdict", answer_id=aid, verdict=verdicts[aid], response=r.text,
                       **{k: v for k, v in r.to_log().items() if k != "text"})

        try:
            await asyncio.gather(*[one(a, t) for a, t in answers.items()])
        finally:
            await client.aclose()
    log.append("judge_end", n=len(verdicts), unparsed=sum(v is None for v in verdicts.values()))
    (args.study / "norms_judge.json").write_text(json.dumps(
        {"mock": args.mock, "model": args.model, "provider": args.provider, "verdicts": verdicts}, indent=2))
    print(f"{len(verdicts)} answers coded ({'mock' if args.mock else args.model}); "
          f"unparsed: {sum(v is None for v in verdicts.values())}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("study", type=Path)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--provider")
    ap.add_argument("--quantization")
    ap.add_argument("--budget-usd", type=float, default=1.0)
    sys.exit(asyncio.run(main(ap.parse_args())))
