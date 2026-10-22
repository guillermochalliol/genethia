"""Run the feasibility pilot.

    python run_pilot.py --mock                                   # full grid, no network
    python run_pilot.py --mock --rounds 4                        # quick check
    python run_pilot.py --conditions C_humanity --seeds 1 --rounds 5   # real, short
    python run_pilot.py --conditions A_none --seeds 1 2 3 --parallel 3  # 3 villages at once

Runs are interleaved (seed-major, conditions alternating) and share one budget.
With --parallel N, up to N villages run at once; they start in that interleaved order.
When the budget stops one run, the others stop at their next call too (same budget).
Each run writes its own hash-chained log; metrics are computed from the logs at the end.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from terrario.conditions import CONDITIONS
from terrario.llm import make_client
from terrario.metrics import collect, format_report
from terrario.orchestrator import Orchestrator

ROOT = Path(__file__).resolve().parent


async def main(args: argparse.Namespace) -> int:
    config = json.loads(args.config.read_text())
    conditions = args.conditions or config["conditions"]
    seeds = args.seeds or config["seeds"]
    rounds = args.rounds or config["rounds"]
    unknown = set(conditions) - set(CONDITIONS)
    if unknown:
        sys.exit(f"unknown conditions: {sorted(unknown)}")

    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = ROOT / config["output_dir"] / f"{config['experiment_name']}-{stamp}{'-mock' if args.mock else ''}"
    out.mkdir(parents=True)
    (out / "config.json").write_text(json.dumps(
        {**config, "cli": {"conditions": conditions, "seeds": seeds, "rounds": rounds, "mock": args.mock}},
        indent=2))

    client = make_client(config, mock=args.mock, seed=args.mock_seed, parallel_runs=args.parallel)
    print(f"{'MOCK' if args.mock else 'REAL'} run -> {out}")
    print(f"budget stop at {client.budget.limit_usd:.2f} USD; "
          f"{len(conditions)} conditions x {len(seeds)} seeds x {rounds} rounds, "
          f"{args.parallel} at a time", flush=True)
    jobs = [(seed, cond) for seed in seeds for cond in conditions]
    slots = asyncio.Semaphore(args.parallel)
    t_all = time.monotonic()

    async def one(seed: int, cond: str) -> str:
        async with slots:
            if client.budget.exhausted:
                return "skipped: budget exhausted"
            t0 = time.monotonic()
            orch = Orchestrator(config, cond, seed, rounds, client, out / f"{cond}_s{seed}")
            reason = await orch.run()
            print(f"  {cond} seed={seed}: {reason} in {time.monotonic() - t0:.1f}s, "
                  f"spent so far {client.budget.spent_usd:.5f} USD", flush=True)
            return reason

    try:
        await asyncio.gather(*[one(s, c) for s, c in jobs])
    finally:
        await client.aclose()
    print(f"wall time {time.monotonic() - t_all:.1f}s", flush=True)

    runs = collect(out)
    (out / "metrics.json").write_text(json.dumps(runs, indent=2))
    report = format_report(runs)
    (out / "report.txt").write_text(report + "\n")
    print("\n" + report)
    return 0 if all(r["log_ok"] for r in runs) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mock", action="store_true", help="simulated models, no API calls")
    ap.add_argument("--mock-seed", type=int, default=0)
    ap.add_argument("--config", type=Path, default=ROOT / "pilot.json")
    ap.add_argument("--conditions", nargs="+")
    ap.add_argument("--seeds", nargs="+", type=int)
    ap.add_argument("--rounds", type=int)
    ap.add_argument("--parallel", type=int, default=1, help="villages running at once")
    sys.exit(asyncio.run(main(ap.parse_args())))
