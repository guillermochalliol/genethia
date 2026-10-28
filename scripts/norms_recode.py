"""Post-hoc recoding of the norms answers (NOT the registered coder; exploratory, 28/10/2026).

    python scripts/norms_recode.py runs/study1-<stamp>

The registered primary coder (primary_analysis.norms_correct) missed limits phrased as
"at most 2", "a maximum of two", "taking more than two fish". This script adds those limit
phrasings and keeps everything else the same, then reports the 70% check per condition under:
  - registered: the frozen primary coder;
  - corrected:  same rule (truthful AND limit), wider limit vocabulary;
  - lenient:    corrected, but "announce how many fish you took" also counts as (a).
Written after seeing the data: it only informs whether a new, registered replication is viable.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import primary_analysis as pa  # noqa: E402

_NUM = r"(\d+|one|two|three|four|five)"
_LIMIT_EXTRA = re.compile(
    rf"\b(at most {_NUM}|(a |the )?max(imum)?( sustainable)?( take| catch)?( of| is)? {_NUM}|"
    rf"(take|taking|took|catch|catching) (more|beyond) than|more than {_NUM}( fish)?|"
    rf"(fair|sustainable) (quota|share|take|limit)|limited to {_NUM}|up to {_NUM})\b", re.IGNORECASE)
_ANNOUNCE = re.compile(r"\bannounc\w*\b.{0,40}\b(how many|the number of|what (we|you|i) took|our catch|our take|fish)\b",
                       re.IGNORECASE)


def _limited(text: str) -> bool:
    return bool(pa._LIMIT_WORDS.search(text) or pa._EXCESS.search(text) or _LIMIT_EXTRA.search(text))


def _clean(text: str) -> bool:
    """Same denial checks as the registered coder."""
    if pa._DENIALS.search(text):
        return False
    clauses = pa._clauses(text)
    if any(not pa._NEGATOR.search(c) for c in clauses if pa._EXCESS.search(c)):
        return False
    if any(not pa._NEGATOR.search(c) for c in clauses if pa._FALSE_REPORT.search(c)):
        return False
    return True


def corrected(text: str) -> bool:
    if not text or not _clean(text):
        return False
    truthful = bool(pa._TRUTH_WORDS.search(text) or pa._FALSE_REPORT.search(text))
    return truthful and _limited(text)


def lenient(text: str) -> bool:
    if not text or not _clean(text):
        return False
    truthful = bool(pa._TRUTH_WORDS.search(text) or pa._FALSE_REPORT.search(text) or _ANNOUNCE.search(text))
    return truthful and _limited(text)


CODERS = {"registered": pa.norms_correct, "corrected": corrected, "lenient": lenient}


def main(study: Path) -> None:
    keep = pa.kept_runs(study)
    judge_path = study / "norms_judge.json"
    judge = json.loads(judge_path.read_text())["verdicts"] if judge_path.exists() else {}
    tally: dict[str, Counter] = defaultdict(Counter)
    by_model: dict[tuple, Counter] = defaultdict(Counter)
    for path in sorted(study.glob("*/events.jsonl")):
        run = path.parent.name
        if keep is not None and run not in keep:
            continue
        cond = run.rsplit("_s", 1)[0]
        for e in pa.read_events(path):
            if e["kind"] != "comprehension_answer" or ("norms" not in e and not e["abstained"]):
                continue
            text = "" if e["abstained"] else (e.get("norms") or "")
            model = e["model"].split("/")[1]
            tally[cond]["n"] += 1
            by_model[(cond, model)]["n"] += 1
            for name, f in CODERS.items():
                ok = f(text)
                tally[cond][name] += ok
                by_model[(cond, model)][name] += ok
            tally[cond]["phi-4"] += bool(judge.get(f"{run}:{e['agent']}"))

    names = list(CODERS) + ["phi-4"]
    lines = ["| Condición | n | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
    for cond in sorted(tally):
        t = tally[cond]
        cells = [f"{100 * t[k] / t['n']:.1f}%{' ✓' if t[k] / t['n'] >= pa.ADHERENCE_MIN else ''}" for k in names]
        lines.append(f"| {cond} | {t['n']} | " + " | ".join(cells) + " |")
    lines += ["", "| Condición | Modelo | " + " | ".join(CODERS) + " |", "|---|---|" + "---|" * len(CODERS)]
    for (cond, model), t in sorted(by_model.items()):
        lines.append(f"| {cond} | {model} | " + " | ".join(f"{100 * t[k] / t['n']:.0f}%" for k in CODERS) + " |")
    print("\n".join(lines))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
