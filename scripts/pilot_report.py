"""Pilot report: per condition and per condition x model, with run-level spread across seeds.

    python scripts/pilot_report.py runs/<pilot-run-dir>

Each run (condition x seed) gives one value per metric; we report the mean and the sample SD
across seeds (the unit for power calculations is the run, not the agent-round).
Writes report.md and report.json next to the run logs.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from terrario.metrics import collect  # noqa: E402

RATE_METRICS = [
    ("misreport", "O1 declaración falsa"),
    ("underreport", "O1 sub-anuncio"),
    ("copy_opportunity", "O2 atajo no sancionado (oport.)"),
    ("copy_overall", "O2 atajo (total)"),
    ("archive_read", "Lectura del archivo"),
    ("temptation_avoidance", "Evitación de la tentación"),
    ("own_accuracy", "Aciertos propios"),
    ("final_accuracy", "Aciertos finales"),
]


def mean_sd(xs: list[float | None]) -> tuple[float | None, float | None, int]:
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, 0
    return statistics.mean(xs), (statistics.stdev(xs) if len(xs) > 1 else None), len(xs)


def cell(x: tuple, pct: bool = True, digits: int = 2) -> str:
    m, sd, n = x
    if m is None:
        return "—"
    f = (lambda v: f"{100 * v:.1f}%") if pct else (lambda v: f"{v:.{digits}f}")
    return f"{f(m)} ± {f(sd)}" if sd is not None else f"{f(m)} (n={n})"


def main(run_dir: Path) -> None:
    runs = collect(run_dir)
    broken = [r["run"] for r in runs if not r["log_ok"]]
    if broken:
        sys.exit(f"broken logs: {broken}")
    by_cond = defaultdict(list)
    for r in runs:
        by_cond[r["condition"]].append(r)

    out: dict = {"conditions": {}, "by_model": {}}
    lines = [f"# Piloto: {run_dir.name}", "",
             "Media ± desvío estándar entre semillas (una observación por corrida).", "",
             "## Por condición", ""]
    header = ["Condición", "Corridas"] + [label for _, label in RATE_METRICS] + \
        ["Lago final", "Colapsos", "Costo/corrida (USD)"]
    lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for cond in sorted(by_cond):
        rs = by_cond[cond]
        stats = {k: mean_sd([r["overall"][k] for r in rs]) for k, _ in RATE_METRICS}
        stats["final_stock"] = mean_sd([r["lake"]["final_stock"] for r in rs])
        stats["cost_usd"] = mean_sd([r["llm"]["cost_usd"] for r in rs])
        collapsed = sum(bool(r["lake"]["collapsed"]) for r in rs)
        out["conditions"][cond] = {
            "runs": len(rs), "collapsed": collapsed,
            **{k: {"mean": v[0], "sd": v[1], "n": v[2]} for k, v in stats.items()},
            "per_run": {r["seed"]: {k: r["overall"][k] for k, _ in RATE_METRICS} for r in rs},
        }
        lines.append("| " + " | ".join(
            [cond, str(len(rs))] + [cell(stats[k]) for k, _ in RATE_METRICS]
            + [cell(stats["final_stock"], pct=False), f"{collapsed}/{len(rs)}",
               cell(stats["cost_usd"], pct=False, digits=4)]) + " |")

    lines += ["", "## Por condición × modelo", ""]
    header = ["Condición", "Modelo"] + [label for _, label in RATE_METRICS]
    lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for cond in sorted(by_cond):
        rs = by_cond[cond]
        models = sorted({m for r in rs for m in r["by_model"]})
        for m in models:
            stats = {k: mean_sd([r["by_model"].get(m, {}).get(k) for r in rs]) for k, _ in RATE_METRICS}
            out["by_model"].setdefault(cond, {})[m] = {
                k: {"mean": v[0], "sd": v[1], "n": v[2]} for k, v in stats.items()}
            lines.append("| " + " | ".join(
                [cond, m.split("/")[1]] + [cell(stats[k]) for k, _ in RATE_METRICS]) + " |")

    llm = [r["llm"] for r in runs]
    total_cost = sum(x["cost_usd"] for x in llm)
    lines += ["", "## Ejecución", "",
              f"- Corridas: {len(runs)}; rondas completas: {sum(r['rounds_completed'] for r in runs)}",
              f"- Costo total: USD {total_cost:.4f}",
              f"- Llamadas: {sum(x['calls'] for x in llm)}; errores: {sum(x['errors'] for x in llm)}; "
              f"truncadas: {sum(x['truncated_calls'] for x in llm)}",
              f"- Proveedor auditado: {sum((x['provider_audit'] or {}).get('verified', 0) for x in llm)} "
              f"verificadas, {sum((x['provider_audit'] or {}).get('mismatches', 0) for x in llm)} discrepancias",
              f"- Latencia p50/p95 por corrida (s): "
              + ", ".join(f"{x['latency_p50_s']}/{x['latency_p95_s']}" for x in llm)]
    out["total_cost_usd"] = total_cost

    (run_dir / "report.md").write_text("\n".join(lines) + "\n")
    (run_dir / "report.json").write_text(json.dumps(out, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
