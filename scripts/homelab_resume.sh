#!/usr/bin/env bash
# Resume the containers paused by scripts/homelab_pause.sh (run by Guille after the batch).
#
#   scripts/homelab_resume.sh
#
# Unpauses only the containers listed in the state file, in reverse order (databases before
# the apps that use them), then expires the Alertmanager silences homelab_pause.sh created.
set -euo pipefail

STATE_FILE="${GENETHIA_PAUSE_STATE:-$HOME/.genethia_paused_containers}"
SILENCE_FILE="${GENETHIA_SILENCE_STATE:-$HOME/.genethia_silences}"
AM_URL="${ALERTMANAGER_URL:-http://localhost:9093}"

expire_silences() {
  [[ -s "$SILENCE_FILE" ]] || return 0
  local ok=1 id
  while read -r id; do
    [[ -z "$id" ]] && continue
    if curl -fsS -X DELETE "$AM_URL/api/v2/silence/$id" >/dev/null; then
      echo "expired  silence $id"
    else
      echo "FAILED   silence $id (it ends on its own after 6 h)" >&2; ok=0
    fi
  done < "$SILENCE_FILE"
  if (( ok == 1 )); then rm -f "$SILENCE_FILE"; fi
}

if [[ ! -s "$STATE_FILE" ]]; then
  echo "No paused-containers state at $STATE_FILE."
  expire_silences
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

# Silences go only after the containers are back, so a slow restart does not page anyone.
expire_silences

if (( failed == 0 )); then
  rm -f "$STATE_FILE"
  echo "All resumed; state file removed."
else
  echo "Some containers failed to resume; state file kept at $STATE_FILE." >&2
  exit 1
fi
