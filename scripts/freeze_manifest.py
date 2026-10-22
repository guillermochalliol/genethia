"""Write FREEZE_MANIFEST.json: SHA-256 of the frozen configuration and of all code.

    python scripts/freeze_manifest.py

The pre-registration attaches the hash of pilot.json and of the code. The project is not a git
repository yet, so this manifest stands in for the commit hash; add the commit once there is one.
"""

import hashlib
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ["pilot.json", "run_pilot.py", "requirements*.txt", "terrario/*.py", "scripts/*.py", "tests/*.py"]


def main() -> None:
    files = sorted({p for pat in PATTERNS for p in ROOT.glob(pat)})
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    tree = hashlib.sha256("".join(f"{k}:{v}\n" for k, v in hashes.items()).encode()).hexdigest()
    manifest = {"created": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "tree_sha256": tree,
                "pilot_json_sha256": hashes["pilot.json"], "files": hashes}
    (ROOT / "FREEZE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"pilot.json {hashes['pilot.json']}\ntree       {tree}\n{len(hashes)} files")


if __name__ == "__main__":
    main()
