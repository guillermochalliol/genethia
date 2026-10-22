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
