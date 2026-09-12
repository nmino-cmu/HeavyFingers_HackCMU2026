#!/bin/bash
# Public URL on orch :80 → Mac serve.py via SSH -R. sk stays on the Mac.
# Usage: source ~/.umbra-vultr.env && umbra/deploy/web-public.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ORCH="${VULTR_ORCH_IP:-207.246.126.149}"
PORT="${UMBRA_WEB_PORT:-8766}"
export UMBRA_WORKER_URL="${UMBRA_WORKER_URL:-http://${ORCH}:8080}"
export UMBRA_WEB_PORT="$PORT"

if ! curl -sS -m 2 -o /dev/null "http://127.0.0.1:${PORT}/"; then
  echo "start serve.py on ${PORT} first" >&2
  exit 1
fi

if ! ssh -o BatchMode=yes -o ConnectTimeout=10 "root@${ORCH}" "ss -ltn | grep -q '127.0.0.1:${PORT}'"; then
  ssh -f -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
    -R "127.0.0.1:${PORT}:127.0.0.1:${PORT}" "root@${ORCH}"
fi
echo "public http://${ORCH}/  http://${ORCH}.sslip.io/"
