"""Action schemas for the pilot round and a tolerant parser for model output.

"Reason freely, constrain late": each action starts with a short free-text
`reasoning` field, then the structured fields. Syntactic validity and semantic
correctness are reported separately, so `parse_action` never repairs values.

Phase 1 (everyone, in parallel): own answer, whether to read the archive,
fish taken, fish announced publicly, a public message.
Phase 2 (only those who read the archive): final answer and whether to tell the village.
"""

from __future__ import annotations

import json
import re
from typing import Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Phase1Action(BaseModel):
    model_config = ConfigDict(extra="ignore")

    reasoning: str = Field(default="", max_length=2000)
    answer: int
    read_archive: bool
    fish_take: int = Field(ge=0, le=5)
    fish_announce: int = Field(ge=0, le=5)
    message: str = Field(default="", max_length=600)


class Phase0Action(BaseModel):
    """Optional separate archive decision, taken before answering (calibration knob `archive_step`)."""

    model_config = ConfigDict(extra="ignore")

    reasoning: str = Field(default="", max_length=2000)
    visit_archive: bool


class RatificationVote(BaseModel):
    """C only: each agent votes on adopting the commitments before round 1."""

    model_config = ConfigDict(extra="ignore")

    reasoning: str = Field(default="", max_length=2000)
    adopt: bool


class ComprehensionAnswer(BaseModel):
    """Asked once per agent after the last round of a completed run (secondary measure)."""

    model_config = ConfigDict(extra="ignore")

    log_contents: str = Field(max_length=600)
    allowed_to_use: Literal["yes", "no", "unsure"]


class ComprehensionNormsAnswer(ComprehensionAnswer):
    """Adds the norms question (manipulation check) in conditions that state norms."""

    norms: str = Field(max_length=600)


class Phase1StepAction(Phase1Action):
    """Phase 1 when the archive decision was already taken in phase 0."""

    read_archive: bool = False


class Phase2Action(BaseModel):
    model_config = ConfigDict(extra="ignore")

    reasoning: str = Field(default="", max_length=2000)
    final_answer: int
    tell_village: bool


A = TypeVar("A", bound=BaseModel)

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_json_object(text: str) -> str | None:
    """Return the first balanced {...} block, preferring fenced code. No eval, ever."""
    m = _FENCE.search(text)
    candidates = [m.group(1), text] if m else [text]
    for cand in candidates:
        start = cand.find("{")
        while start != -1:
            depth, in_str, esc = 0, False, False
            for i in range(start, len(cand)):
                ch = cand[i]
                if in_str:
                    if esc:
                        esc = False
                    elif ch == "\\":
                        esc = True
                    elif ch == '"':
                        in_str = False
                elif ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return cand[start : i + 1]
            start = cand.find("{", start + 1)
    return None


def parse_action(text: str, schema: type[A]) -> tuple[A | None, str | None]:
    """Return (action, None) on success or (None, error_code: detail) on failure."""
    raw = extract_json_object(text or "")
    if raw is None:
        return None, "NO_JSON"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f"BAD_JSON: {e.msg}"
    if not isinstance(data, dict):
        return None, "NOT_OBJECT"
    try:
        return schema.model_validate(data), None
    except ValidationError as e:
        fields = ",".join(".".join(str(p) for p in err["loc"]) for err in e.errors())
        return None, f"SCHEMA: {fields}"
