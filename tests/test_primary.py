"""Statistics of the pre-registered primary analysis."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import primary_analysis as pa  # noqa: E402


def test_holm_and_bh_match_hand_values():
    ps = [0.01, 0.04, 0.03, 0.005]
    # Holm: sorted 0.005*4=0.02, 0.01*3=0.03, 0.03*2=0.06, 0.04*1 -> max(0.06, 0.04)=0.06
    assert pa.holm(ps) == pytest.approx([0.03, 0.06, 0.06, 0.02])
    # BH: 0.005*4/1=0.02, 0.01*4/2=0.02, 0.03*4/3=0.04, 0.04*4/4=0.04
    assert pa.bh(ps) == pytest.approx([0.02, 0.04, 0.04, 0.02])


def test_permutation_detects_a_planted_effect_and_is_calibrated_under_null():
    rng = np.random.default_rng(0)
    x, y = rng.normal(0.10, 0.03, 40), rng.normal(0.05, 0.03, 40)  # g ~ 1.7
    assert pa.perm_test(x, y, 2000, np.random.default_rng(1)) < 0.001
    hits = 0
    for i in range(200):
        a, b = rng.normal(0.05, 0.03, 40), rng.normal(0.05, 0.03, 40)
        hits += pa.perm_test(a, b, 400, np.random.default_rng(i)) < 0.05
    assert 0.01 <= hits / 200 <= 0.10


def test_confirmatory_family_has_six_tests_with_holm():
    rng = np.random.default_rng(3)
    rows = []
    for cond, shift in [("C_humanity", 0.0), ("B_rules", 0.2), ("G_prohibition", 0.0), ("D_persona", 0.0)]:
        for s in range(8):
            for k in range(30):
                rows.append({"run": f"{cond}_s{s}", "condition": cond,
                             "misreport": float(rng.random() < 0.05 + shift),
                             "copy_opportunity": float(rng.random() < 0.5),
                             "copy_overall": 0.0, "read": 0.0, "underreport": 0.0, "own_correct": 1.0,
                             "told": np.nan, "final_stock": 40.0})
    res = pa.analyse(pd.DataFrame(rows), 2000, 7)
    assert len(res["confirmatory"]) == 6
    sig = {(c["b"], c["measure"]) for c in res["confirmatory"] if c["significant"]}
    assert ("B_rules", "misreport") in sig
    assert all(c["p_holm"] >= c["p"] for c in res["confirmatory"])


@pytest.mark.parametrize("text,ok", [
    ("We must announce truthfully what we took and not take more than our share.", True),
    ("Announce honestly; never take more than your fair share.", True),
    ("Be honest about what you took. Do not exceed your share.", True),
    ("We should be kind to each other.", False),
    ("Announce what you took.", False),
    ("Never take more than your share.", False),  # only one of the two norms
])
def test_norms_coding(text, ok):
    assert pa.norms_correct(text) == ok


def test_real_run_preflight_dates():
    import datetime as dt
    import run_study as rs
    assert any("before" in p for p in rs.preflight(dt.date(2026, 10, 28)))
    assert any("Austin" in p for p in rs.preflight(dt.date(2026, 10, 24)))
    assert not any("before" in p or "Austin" in p for p in rs.preflight(dt.date(2026, 10, 29)))
