#!/usr/bin/env bash
# Resume the containers paused by scripts/homelab_pause.sh (run by Guille after the batch).
#
#   scripts/homelab_resume.sh
#
# Unpauses only the containers listed in the state file, in reverse order (databases before
# the apps that use them), then removes the state file.
set -euo pipefail

STATE_FILE="${GENETHIA_PAUSE_STATE:-$HOME/.genethia_paused_containers}"

if [[ ! -s "$STATE_FILE" ]]; then
  echo "No state file at $STATE_FILE: nothing paused by homelab_pause.sh." >&2
  exit 0
fi

mapfile -t paused < "$STATE_FILE"
failed=0
for (( i=${#paused[@]}-1; i>=0; i-- )); do
  name="${paused[$i]}"
  [[ -z "$name" ]] && continue
  status=$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || echo "missing")
  if [[ "$status" == "paused" ]]; then
    if docker unpause "$name" >/dev/null; then echo "resumed  $name"; else echo "FAILED   $name" >&2; failed=1; fi
  else
    echo "skip     $name ($status)"
  fi
done

if (( failed == 0 )); then
  rm -f "$STATE_FILE"
  echo "All resumed; state file removed."
else
  echo "Some containers failed to resume; state file kept at $STATE_FILE." >&2
  exit 1
fi
