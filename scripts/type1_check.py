"""Type I error check of the primary analysis: shuffle condition labels across runs and re-test.

    python scripts/type1_check.py runs/study1-<stamp>-mock [--iters 200] [--perms 2000]

Run-level outcomes are computed once; each iteration permutes the condition labels across all
kept runs (group sizes preserved), runs the 6 confirmatory permutation tests (C vs B, C vs G,
C vs D on O1 and O2) and applies Holm. With the null true by construction, the share of
significant tests should be ~5% before Holm and the family-wise rate <= 5% after Holm.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import primary_analysis as pa  # noqa: E402
from analyze import agent_rounds  # noqa: E402


def confirmatory_ps(runs, perms: int, rng) -> list[float]:
    ps = []
    for a, b in pa.CONFIRMATORY:
        for col in pa.PRIMARY:
            x = runs.loc[runs.condition == a, col].dropna().to_numpy(dtype=float)
            y = runs.loc[runs.condition == b, col].dropna().to_numpy(dtype=float)
            ps.append(pa.perm_test(x, y, perms, rng))
    return ps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("study", type=Path)
    ap.add_argument("--iters", type=int, default=200)
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    rows = agent_rounds(args.study)
    keep = pa.kept_runs(args.study)
    if keep is not None:
        rows = rows[rows.run.isin(keep)]
    runs = pa.run_level(rows)
    rng = np.random.default_rng(args.seed)
    raw = np.zeros((args.iters, 6))
    adj = np.zeros((args.iters, 6))
    for i in range(args.iters):
        shuffled = runs.copy()
        shuffled["condition"] = rng.permutation(shuffled["condition"].to_numpy())
        ps = confirmatory_ps(shuffled, args.perms, rng)
        raw[i], adj[i] = ps, pa.holm(ps)
    labels = [f"{b} {m}" for _, b in pa.CONFIRMATORY for m in pa.PRIMARY]
    out = {
        "study": args.study.name, "iters": args.iters, "perms": args.perms,
        "runs_per_condition": runs.groupby("condition").size().to_dict(),
        "share_significant_raw": float((raw < 0.05).mean()),
        "share_significant_holm": float((adj < 0.05).mean()),
        "familywise_raw": float((raw < 0.05).any(axis=1).mean()),
        "familywise_holm": float((adj < 0.05).any(axis=1).mean()),
        "per_test_raw": dict(zip(labels, (raw < 0.05).mean(axis=0).round(4).tolist())),
    }
    (args.study / "type1_check.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
