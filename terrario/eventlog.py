"""Append-only, hash-chained event log (JSON Lines).

Each line stores the event plus `prev_hash` and `hash`, where
hash = SHA-256(prev_hash || canonical_json(event_without_hashes)).
Editing or deleting any line breaks the chain, which `verify_log` detects.
This makes tampering detectable, not impossible: anchor the last hash
somewhere outside the box (e.g., copy the head file, `head.txt` or `<log>_head.txt`, off the
server) for stronger guarantees.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

GENESIS = "0" * 64


def _canonical(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _digest(prev_hash: str, payload: dict[str, Any]) -> str:
    return hashlib.sha256((prev_hash + _canonical(payload)).encode("utf-8")).hexdigest()


class EventLog:
    """Append-only writer. Only this class writes to the log file."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # One head file per log, so several logs can share a folder (a study folder holds the
        # ledger and the judge log). Run logs keep the historical name head.txt.
        name = "head.txt" if path.name == "events.jsonl" else f"{path.stem}_head.txt"
        self.head_path = path.parent / name
        self._prev = GENESIS
        self._seq = 0
        if self.path.exists():
            # Resume the chain from the last line.
            ok, last_hash, count, _ = verify_log(self.path)
            if not ok:
                raise RuntimeError(f"Refusing to append to a broken log: {self.path}")
            self._prev, self._seq = last_hash, count

    def append(self, kind: str, **data: Any) -> dict[str, Any]:
        payload = {"seq": self._seq, "ts": round(time.time(), 3), "kind": kind, **data}
        h = _digest(self._prev, payload)
        record = {**payload, "prev_hash": self._prev, "hash": h}
        # Open in append mode for every write: no handle that could seek or truncate.
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self._prev = h
        self._seq += 1
        self.head_path.write_text(f"{self._seq} {h}\n")
        return record


def verify_log(path: Path) -> tuple[bool, str, int, str]:
    """Return (ok, last_hash, n_events, message)."""
    prev = GENESIS
    n = 0
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            rec = json.loads(line)
            stored_prev, stored_hash = rec.pop("prev_hash"), rec.pop("hash")
            if stored_prev != prev:
                return False, prev, n, f"BROKEN_LINK at line {lineno}"
            if _digest(prev, rec) != stored_hash:
                return False, prev, n, f"HASH_MISMATCH at line {lineno}"
            if rec.get("seq") != n:
                return False, prev, n, f"SEQ_GAP at line {lineno}"
            prev = stored_hash
            n += 1
    return True, prev, n, "OK"


def read_events(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]
