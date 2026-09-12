#!/bin/bash
# Sync static desk to orch nginx (/var/www/umbra). sk stays on the Mac.
# Usage: umbra/deploy/web-public.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ORCH="${VULTR_ORCH_IP:-207.246.126.149}"
rsync -az --exclude serve.py --exclude '__pycache__' --exclude '*.pyc' \
  "$ROOT/umbra/web/" "root@${ORCH}:/var/www/umbra/"
echo "public http://${ORCH}/  http://${ORCH}.sslip.io/"
