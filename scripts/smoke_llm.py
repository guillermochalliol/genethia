"""One tiny call per pilot model: checks pinning, served provider, cost and latency.

    python scripts/smoke_llm.py --mock      # no network, no credits
    python scripts/smoke_llm.py             # real: needs OPENROUTER_API_KEY, costs well under 0.01 USD
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from terrario.actions import Phase2Action, parse_action  # noqa: E402
from terrario.llm import make_client  # noqa: E402

PROMPT = (
    "A fisher fills 3 baskets with 4 fish each and sells 5. How many fish are left?\n"
    'Reply only with JSON: {"reasoning": "<one short sentence>", "final_answer": <integer>, '
    '"tell_village": false}'
)


async def main(mock: bool, config_path: Path) -> int:
    config = json.loads(config_path.read_text())
    client = make_client(config, mock=mock)
    models = sorted({m["model"] for m in config["village"]["members"]})
    try:
        results = await asyncio.gather(
            *[client.complete(m, [{"role": "user", "content": PROMPT}]) for m in models],
            return_exceptions=True,
        )
    finally:
        await client.aclose()
    failed = 0
    for model, r in zip(models, results):
        if isinstance(r, Exception):
            failed += 1
            print(f"FAIL {model}: {r}")
            continue
        action, err = parse_action(r.text, Phase2Action)
        print(
            f"{'OK  ' if r.provider_ok else 'WARN'} {model}\n"
            f"     provider={r.provider} ({r.provider_source}) cost={r.cost_usd:.6f} USD "
            f"latency={r.latency_s}s tokens={r.prompt_tokens}+{r.completion_tokens}\n"
            f"     parsed={action.model_dump() if action else err}"
        )
        failed += not r.provider_ok
    print("budget:", client.budget.snapshot())
    return 1 if failed else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "pilot.json")
    args = ap.parse_args()
    sys.exit(asyncio.run(main(args.mock, args.config)))
