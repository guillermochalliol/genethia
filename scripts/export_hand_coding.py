"""Export a random sample of norms answers for blind hand coding (pre-registration section 5).

    python scripts/export_hand_coding.py runs/study1-<stamp> [--n 100] [--seed 20261023]

Writes, in the study folder:
  hand_coding.csv       id, answer, correct (empty: fill with 1 or 0), notes
                        No condition, model or run: the coder sees only the answer.
  hand_coding_key.json  id -> answer_id ("<run>:<agent>"), to merge the codes back later.
Do not open the key file while coding.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from norms_judge import norms_answers  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("study", type=Path)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261023)
    args = ap.parse_args()

    answers = norms_answers(args.study)
    ids = sorted(answers)
    sample = random.Random(args.seed).sample(ids, min(args.n, len(ids)))
    key = {}
    rows = []
    for aid in sample:
        hid = "H" + hashlib.sha256(f"{args.seed}:{aid}".encode()).hexdigest()[:8]
        key[hid] = aid
        rows.append({"id": hid, "answer": answers[aid], "correct": "", "notes": ""})
    rows.sort(key=lambda r: r["id"])  # order unrelated to condition or run
    with open(args.study / "hand_coding.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "answer", "correct", "notes"])
        w.writeheader()
        w.writerows(rows)
    (args.study / "hand_coding_key.json").write_text(json.dumps(
        {"seed": args.seed, "n": len(rows), "key": key}, indent=2))
    print(f"{len(rows)} answers -> {args.study / 'hand_coding.csv'} (key in hand_coding_key.json)")


if __name__ == "__main__":
    main()
