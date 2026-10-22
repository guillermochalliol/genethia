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
#
# Before pausing, it creates two 6-hour Alertmanager silences (API v2), scoped to the paused
# monitoring services only, and records their IDs so homelab_resume.sh can expire them:
#   1. name=~"hd-cadvisor|hd-loki|hd-promtail"  (container alerts carry the container name)
#   2. job="cadvisor"                            (the only one of the three scraped by Prometheus)
# Checked 22/10/2026: loki and promtail are not Prometheus targets and no rule alerts on them;
# ContainerDown/ContainerRestarting are computed from cadvisor metrics, so while cadvisor is
# paused they cannot fire for ANY container (f1pedia included).
set -euo pipefail

STATE_FILE="${GENETHIA_PAUSE_STATE:-$HOME/.genethia_paused_containers}"
SILENCE_FILE="${GENETHIA_SILENCE_STATE:-$HOME/.genethia_silences}"
AM_URL="${ALERTMANAGER_URL:-http://localhost:9093}"
SILENCE_HOURS=6

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

# JSON body for one silence: $1 label name, $2 value, $3 isRegex (true|false).
silence_json() {
  local start end
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  end=$(date -u -d "+${SILENCE_HOURS} hours" +%Y-%m-%dT%H:%M:%SZ)
  printf '{"matchers":[{"name":"%s","value":"%s","isRegex":%s,"isEqual":true}],' "$1" "$2" "$3"
  printf '"startsAt":"%s","endsAt":"%s","createdBy":"genethia homelab_pause.sh",' "$start" "$end"
  printf '"comment":"Genethia Study 1 batch: monitoring containers paused to free memory"}'
}
# label|value|isRegex (the value may itself contain '|', it is split from both ends).
SILENCES=(
  "name|hd-cadvisor|hd-loki|hd-promtail|true"
  "job|cadvisor|false"
)

dry=false
[[ "${1:-}" == "--dry" ]] && dry=true

echo "Free memory before: $(mem_free)"
if [[ -s "$STATE_FILE" || -s "$SILENCE_FILE" ]] && ! $dry; then
  echo "State files already exist ($STATE_FILE / $SILENCE_FILE); run homelab_resume.sh first." >&2
  exit 1
fi

# Silences first: if Alertmanager is unreachable, stop before pausing anything.
for spec in "${SILENCES[@]}"; do
  label=${spec%%|*}; rest=${spec#*|}; is_regex=${rest##*|}; value=${rest%|*}
  op="="; [[ $is_regex == true ]] && op="=~"
  body=$(silence_json "$label" "$value" "$is_regex")
  if $dry; then
    echo "would create silence (${SILENCE_HOURS} h): ${label}${op}\"${value}\""
    echo "  POST $AM_URL/api/v2/silences $body"
  else
    id=$(curl -fsS -X POST -H 'Content-Type: application/json' -d "$body" "$AM_URL/api/v2/silences" \
         | sed -n 's/.*"silenceID":"\([^"]*\)".*/\1/p')
    if [[ -z "$id" ]]; then
      echo "Could not create silence for $label; nothing paused." >&2
      exit 1
    fi
    echo "$id" >> "$SILENCE_FILE"
    echo "silenced ${label}${op}\"${value}\" (${SILENCE_HOURS} h, id $id)"
  fi
done

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
