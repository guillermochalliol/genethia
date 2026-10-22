#!/usr/bin/env bash
# Pause homelab containers to free memory for the Study 1 batch (run by Guille, not by the runner).
#
#   scripts/homelab_pause.sh          # pause, then show free memory
#   scripts/homelab_pause.sh --dry    # only show what would be paused
#
# Uses `docker pause` (processes frozen, memory kept resident but reclaimable; state intact).
# Apps are paused before their databases. Only containers this script actually paused are
# recorded in the state file, so scripts/homelab_resume.sh unpauses exactly those.
# Never touches F1/f1pedia, client sites (att, pili, workspace) or the homelab MCP access.
set -euo pipefail

STATE_FILE="${GENETHIA_PAUSE_STATE:-$HOME/.genethia_paused_containers}"

# Order matters: apps first, then their databases / search / cache.
TARGETS=(
  auto-temporal auto-temporal-es auto-temporal-db
  auto-n8n
  auto-postiz auto-postiz-redis auto-postiz-db
  auto-listmonk auto-listmonk-db
  auto-job-runner
  perkins
  hd-cadvisor hd-promtail hd-loki
)
# Safety net in case the list above is ever edited by mistake.
PROTECTED_REGEX='^(f1|f2|hd-f1|hd-race|att|pili|workspace|auto-mcp|auto-socket-proxy|hd-prometheus|hd-alertmanager)'

mem_free() { awk '/MemAvailable/ {printf "%.1f GiB", $2/1024/1024}' /proc/meminfo; }

dry=false
[[ "${1:-}" == "--dry" ]] && dry=true

echo "Free memory before: $(mem_free)"
if [[ -s "$STATE_FILE" ]] && ! $dry; then
  echo "State file $STATE_FILE already lists paused containers; run homelab_resume.sh first." >&2
  exit 1
fi

paused=()
for name in "${TARGETS[@]}"; do
  if [[ "$name" =~ $PROTECTED_REGEX ]]; then
    echo "REFUSED  $name (protected)" >&2
    continue
  fi
  status=$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || echo "missing")
  case "$status" in
    running)
      if $dry; then
        echo "would pause  $name"
      else
        docker pause "$name" >/dev/null && echo "paused   $name" && paused+=("$name")
      fi
      ;;
    paused) echo "skip     $name (already paused, not recorded)" ;;
    *)      echo "skip     $name ($status)" ;;
  esac
done

if ! $dry; then
  if (( ${#paused[@]} > 0 )); then printf '%s\n' "${paused[@]}" > "$STATE_FILE"; fi
  sleep 3
  echo "Paused ${#paused[@]} containers (list in $STATE_FILE)."
fi
echo "Free memory after: $(mem_free)  (Study 1 runner needs >= 2.5 GiB)"
