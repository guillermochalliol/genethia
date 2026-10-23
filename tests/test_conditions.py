"""Condition texts: length matching (pre-registration section 3) and no archive mentions (D2)."""

import pytest

from terrario.conditions import CONDITIONS, LENGTH_MATCHED

C = CONDITIONS["C_humanity"]


@pytest.mark.parametrize("name", LENGTH_MATCHED)
def test_matched_to_c(name):
    t = CONDITIONS[name]
    assert abs(len(t) / len(C) - 1) <= 0.03
    assert abs(len(t.split()) / len(C.split()) - 1) <= 0.03


@pytest.mark.parametrize("name", list(CONDITIONS))
def test_no_condition_mentions_the_archive(name):
    low = CONDITIONS[name].lower()
    assert not any(w in low for w in ("archive", "record", "verification", "checker"))


def test_persona_texts_have_no_institutions():
    for name in ("D_persona", "F_rich_persona"):
        low = CONDITIONS[name].lower()
        assert not any(w in low for w in ("rule", "vote", "assembly", "commit", "curious"))
    assert "cheat" not in CONDITIONS["F_rich_persona"].lower()


def test_g_is_an_explicit_prohibition_and_h_is_imposed():
    assert "not permitted" in CONDITIONS["G_prohibition"] and "under any circumstances" in CONDITIONS["G_prohibition"]
    assert "administrators" in CONDITIONS["H_explained_imposed"]
    assert "because" in CONDITIONS["H_explained_imposed"]


# Annex A of the pre-registration (D4a): B, G, H and C cover exactly these five points.
NORM_TEXTS = ["B_rules", "G_prohibition", "H_explained_imposed", "C_humanity"]
ANNEX_A = {
    "1 truthful reports": [r"misreport|tell the truth", r"question (another member's |an )announcement"],
    "2 scores and answers": [r"alter scores", r"another member's answer"],
    "3 share and replacement": [r"more than (your|our) share", r"(stock|lake) can replace"],
    "4 no pressure": [r"pressure (any member|anyone)"],
    "5 priority and no harm": [r"fewest points", r"harm the village or the people who run this world"],
}


@pytest.mark.parametrize("name", NORM_TEXTS)
@pytest.mark.parametrize("point", list(ANNEX_A))
def test_annex_a_point_in_every_norm_text(name, point):
    import re
    for pattern in ANNEX_A[point]:
        assert re.search(pattern, CONDITIONS[name], re.IGNORECASE), (name, point, pattern)


@pytest.mark.parametrize("name", NORM_TEXTS)
def test_exactly_five_points_and_reasons_only_in_h_and_c(name):
    import re
    assert re.findall(r"^\d\. ", CONDITIONS[name], re.MULTILINE) == [f"{i}. " for i in range(1, 6)]
    has_reasons = "because" in CONDITIONS[name]
    assert has_reasons == (name in ("H_explained_imposed", "C_humanity"))
