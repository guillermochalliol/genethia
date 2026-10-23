"""Check real per-model token counts of every condition text (pre-registration section 3).

    python scripts/token_check.py [--mock]

For each model, sends the real system prompt once per condition (plus once with an empty
condition) with max_tokens=1, and records usage.prompt_tokens in a hash-chained log.
Condition tokens = prompt_tokens(condition) - prompt_tokens(empty). This is a tokenizer check,
not an experimental run: no rounds, no agents acting.
C is measured WITHOUT the vote-result line the orchestrator appends from round 1 on (D4b):
that line is part of the manipulation and stays outside the length check.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from terrario import prompts  # noqa: E402
from terrario.conditions import CONDITIONS, LENGTH_MATCHED  # noqa: E402
from terrario.eventlog import EventLog  # noqa: E402
from terrario.llm import make_client  # noqa: E402


async def main(mock: bool) -> int:
    config = json.loads((ROOT / "pilot.json").read_text())
    cfg = copy.deepcopy(config)
    cfg["llm"]["max_tokens"] = 1
    client = make_client(cfg, mock=mock)
    out = ROOT / config["output_dir"] / f"token-check-{time.strftime('%Y%m%d-%H%M%S')}{'-mock' if mock else ''}"
    log = EventLog(out / "events.jsonl")
    models = sorted({m["model"] for m in config["village"]["members"]})
    n = len(config["village"]["members"])
    texts = {"(empty)": "", **CONDITIONS}

    async def one(model: str, name: str):
        msgs = [{"role": "system", "content": prompts.system_prompt("A1", n, texts[name], config["world"])},
                {"role": "user", "content": "Reply with OK."}]
        r = await client.complete(model, msgs)
        log.append("token_check", model=model, condition=name, prompt_tokens=r.prompt_tokens,
                   provider=r.provider, cost_usd=r.cost_usd, mock=r.mock)
        return model, name, r.prompt_tokens

    try:
        res = await asyncio.gather(*[one(m, c) for m in models for c in texts])
    finally:
        await client.aclose()
    tok = {(m, c): t for m, c, t in res}
    table = {}
    print(f"{'condition':<22}" + "".join(f"{m.split('/')[1][:14]:>16}" for m in models))
    for c in CONDITIONS:
        row = {}
        for m in models:
            k = tok[(m, c)] - tok[(m, "(empty)")]
            ref = tok[(m, "C_humanity")] - tok[(m, "(empty)")]
            row[m] = {"tokens": k, "vs_C": round(k / ref - 1, 4)}
        table[c] = row
        print(f"{c:<22}" + "".join(f"{row[m]['tokens']:>9} ({100 * row[m]['vs_C']:+5.1f}%)" for m in models))
    bad = [(c, m) for c in LENGTH_MATCHED for m in models if abs(table[c][m]["vs_C"]) > 0.03]
    log.append("token_check_summary", table=table, outside_3pct=bad,
               note="C measured without the vote-result line (D4b)")
    (out / "token_check.json").write_text(json.dumps(table, indent=2))
    print("note: C measured without the vote-result line (part of the manipulation, D4b)")
    print("outside ±3% of C:", bad or "none", f"\nlog: {out}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mock", action="store_true")
    sys.exit(asyncio.run(main(ap.parse_args().mock)))
