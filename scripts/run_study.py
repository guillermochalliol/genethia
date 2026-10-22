"""Run Study 1 with the pre-registered exclusion and replacement rules.

    python scripts/run_study.py --mock --n-runs 3 --rounds 5 --parallel 8   # dry run
    python scripts/run_study.py --parallel 6                                 # confirmatory (40/cond)

Seeds 1..n_runs per condition, interleaved in time (seed-major, conditions alternating).
After each run the exclusion rules (terrario/exclusions.py) are applied from its log; an
excluded run is replaced by that condition's next reserve seed (41, 42, ...). Every decision
goes to a hash-chained ledger (study_ledger.jsonl); all runs, kept or not, stay on disk.
The study stops if the shared budget is exhausted (then it is reported as incomplete).
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from terrario.conditions import CONDITIONS  # noqa: E402
from terrario.eventlog import EventLog, read_events, verify_log  # noqa: E402
from terrario.exclusions import evaluate_run  # noqa: E402
from terrario.llm import MockBehavior, MockClient, make_client  # noqa: E402
from terrario.orchestrator import Orchestrator  # noqa: E402

# Guards for real (non-mock) runs, decided by Guille on 22/10/2026:
# not before 29/10/2026 (waiting for sinc(i)); never on the Austin GP weekend (the homelab needs
# its memory then; 2026 US GP: 23-25/10, checked on racingnews365.com); at least 2.5 GiB free
# (lowered from 4 GiB on 22/10/2026: the runner itself uses ~40 MB).
EARLIEST_REAL_RUN = dt.date(2026, 10, 29)
BLOCKED_DATES = {dt.date(2026, 10, 23), dt.date(2026, 10, 24), dt.date(2026, 10, 25)}
MIN_FREE_GIB = 2.5


def mem_available_gib() -> float:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1024**2
    raise RuntimeError("MemAvailable not found in /proc/meminfo")


def preflight(today: dt.date | None = None) -> list[str]:
    """Reasons not to start a real run now (empty list = go)."""
    today = today or dt.date.today()
    problems = []
    if today < EARLIEST_REAL_RUN:
        problems.append(f"before {EARLIEST_REAL_RUN} (waiting for sinc(i))")
    if today in BLOCKED_DATES:
        problems.append("Austin GP weekend: the homelab needs its memory")
    free = mem_available_gib()
    if free < MIN_FREE_GIB:
        problems.append(f"only {free:.1f} GiB free (< {MIN_FREE_GIB} GiB)")
    return problems


STUDY_CONDITIONS = ["A_none", "B_rules", "C_humanity", "D_persona", "E_filler",
                    "F_rich_persona", "G_prohibition", "H_explained_imposed"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def main(args: argparse.Namespace) -> int:
    config = json.loads(args.config.read_text())
    if config.get("calibration", {}).get("status") != "FROZEN":
        sys.exit("pilot.json is not frozen")
    conditions = args.conditions or STUDY_CONDITIONS
    assert set(conditions) <= set(CONDITIONS), set(conditions) - set(CONDITIONS)
    if not args.mock:
        problems = preflight()
        if problems:
            sys.exit("not starting a real run: " + "; ".join(problems))
        print(f"preflight ok: {mem_available_gib():.1f} GiB free", flush=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = ROOT / config["output_dir"] / f"study1-{stamp}{'-mock' if args.mock else ''}"
    out.mkdir(parents=True)
    ledger = EventLog(out / "study_ledger.jsonl")
    ledger.append("study_start", conditions=conditions, n_runs=args.n_runs, rounds=args.rounds,
                  reserve_start=args.reserve_start, parallel=args.parallel, mock=args.mock,
                  config_sha256=sha256(args.config), config=config)

    if args.mock:
        behavior = MockBehavior(p_invalid=args.mock_p_invalid)
        client = MockClient(make_client(config, mock=True).budget, behavior=behavior)
    else:
        client = make_client(config, mock=False, parallel_runs=args.parallel)

    queue: asyncio.Queue = asyncio.Queue()
    for seed in range(1, args.n_runs + 1):
        for cond in conditions:
            queue.put_nowait((cond, seed, "planned"))
    next_reserve = {c: args.reserve_start for c in conditions}
    valid: dict[str, list[int]] = {c: [] for c in conditions}
    stop = asyncio.Event()

    async def worker() -> None:
        while True:
            cond, seed, kind = await queue.get()
            try:
                if stop.is_set():
                    ledger.append("run_skipped", condition=cond, seed=seed, run_kind=kind, reason="study stopped")
                    continue
                run_dir = out / f"{cond}_s{seed}"
                t0 = time.monotonic()
                reason = await Orchestrator(config, cond, seed, args.rounds, client, run_dir).run()
                ok, _, _, msg = verify_log(run_dir / "events.jsonl")
                verdict = evaluate_run(read_events(run_dir / "events.jsonl")) if ok else \
                    {"excluded": True, "reasons": [f"broken log: {msg}"]}
                ledger.append("run_done", condition=cond, seed=seed, run_kind=kind, end_reason=reason,
                              seconds=round(time.monotonic() - t0, 1), **verdict,
                              spent_usd=round(client.budget.spent_usd, 6))
                if not verdict["excluded"]:
                    valid[cond].append(seed)
                elif client.budget.exhausted:
                    stop.set()
                elif next_reserve[cond] >= args.reserve_start + args.max_reserves:
                    ledger.append("reserve_exhausted", condition=cond, excluded_seed=seed)
                else:
                    reserve = next_reserve[cond]
                    next_reserve[cond] += 1
                    ledger.append("replacement", condition=cond, excluded_seed=seed, reserve_seed=reserve)
                    queue.put_nowait((cond, reserve, "reserve"))
                print(f"  {cond} s{seed} ({kind}): {'EXCLUDED ' + '; '.join(verdict['reasons']) if verdict['excluded'] else 'ok'}"
                      f"  [{client.budget.spent_usd:.4f} USD]", flush=True)
            except Exception as e:  # never let a dead worker hang the queue
                ledger.append("worker_error", condition=cond, seed=seed, error=f"{type(e).__name__}: {e}")
                print(f"  {cond} s{seed}: WORKER ERROR {type(e).__name__}: {e}", flush=True)
                stop.set()
            finally:
                queue.task_done()

    print(f"{'MOCK' if args.mock else 'REAL'} study -> {out}", flush=True)
    t_all = time.monotonic()
    workers = [asyncio.create_task(worker()) for _ in range(args.parallel)]
    try:
        await queue.join()
    finally:
        for w in workers:
            w.cancel()
        await client.aclose()
    complete = all(len(v) >= args.n_runs for v in valid.values())
    ledger.append("study_end", complete=complete, valid={c: sorted(v) for c, v in valid.items()},
                  wall_seconds=round(time.monotonic() - t_all, 1), budget=client.budget.snapshot())
    print(f"\n{'complete' if complete else 'INCOMPLETE'}: "
          + ", ".join(f"{c}={len(v)}" for c, v in valid.items())
          + f"; {time.monotonic() - t_all:.0f}s; {client.budget.spent_usd:.4f} USD")
    return 0 if complete else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, default=ROOT / "pilot.json")
    ap.add_argument("--conditions", nargs="+")
    ap.add_argument("--n-runs", type=int, default=40)
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--reserve-start", type=int, default=41)
    ap.add_argument("--parallel", type=int, default=6)
    ap.add_argument("--max-reserves", type=int, default=20, help="per condition")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--mock-p-invalid", type=float, default=0.08,
                    help="mock only: raise it to exercise the abstention exclusion")
    sys.exit(asyncio.run(main(ap.parse_args())))
