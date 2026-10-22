"""Pre-registered exclusion rules (pre-registration section 7), computed only from a run's log.

A run is excluded, and replaced with the next reserve seed of its condition, if:
  1. more than 2% of its agent decisions have no valid response (abstentions after retries,
     including calls that failed for good, and C's ratification votes; the post-run
     comprehension questions are not game decisions and do not count);
  2. any call was served by a provider other than the pinned one (response field or audit);
  3. it was cut short (budget, technical error, missing run_end, fewer rounds than planned).
A run is never excluded because of its results.
"""

from __future__ import annotations

from typing import Any

MAX_ABSTENTION = 0.02


def evaluate_run(events: list[dict[str, Any]]) -> dict[str, Any]:
    start = next(e for e in events if e["kind"] == "run_start")
    end = next((e for e in events if e["kind"] == "run_end"), None)
    decisions = [e for e in events if e["kind"] in ("action", "ratification_vote")]
    abstained = sum(1 for e in decisions if e["abstained"])
    rate = abstained / len(decisions) if decisions else 1.0
    wrong_provider = sum(1 for e in events if e["kind"] == "llm_call" and not e["provider_ok"])
    audit = next((e for e in events if e["kind"] == "provider_audit"), None)
    audit_mismatch = len(audit["mismatches"]) if audit else 0
    rounds_done = sum(1 for e in events if e["kind"] == "round_end")

    reasons = []
    if rate > MAX_ABSTENTION:
        reasons.append(f"abstention {rate:.1%} > {MAX_ABSTENTION:.0%}")
    if wrong_provider or audit_mismatch:
        reasons.append(f"provider mismatch ({wrong_provider} in responses, {audit_mismatch} in audit)")
    if end is None or end["reason"] != "completed" or rounds_done < start["rounds"]:
        reasons.append(f"technical cut ({end['reason'] if end else 'no run_end'}, "
                       f"{rounds_done}/{start['rounds']} rounds)")
    return {
        "excluded": bool(reasons),
        "reasons": reasons,
        "decisions": len(decisions),
        "abstained": abstained,
        "abstention_rate": round(rate, 4),
        "provider_unverified": len(audit["unverified"]) if audit else None,
    }
