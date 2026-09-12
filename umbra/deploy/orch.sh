#!/bin/bash
set -euo pipefail
source "$HOME/.umbra-vultr.env"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ssh -o BatchMode=yes "root@$VULTR_ORCH_IP" "mkdir -p /opt/umbra; ufw allow 8080/tcp; ufw allow from 10.20.0.0/24; ufw --force enable"
scp "$ROOT/umbra/orch/app.py" "root@$VULTR_ORCH_IP:/opt/umbra/app.py"
ssh -o BatchMode=yes "root@$VULTR_ORCH_IP" "systemctl stop umbra-orch-smoke 2>/dev/null || true
pkill -f '/opt/umbra/app.py' || true
pkill -f 'http.server 8080' || true
UMBRA_FHE_UPSTREAM=http://$UMBRA_FHE_VPC_IP:8081 nohup python3 /opt/umbra/app.py >/tmp/orch.log 2>&1 &
sleep 1
ss -ltnp | grep 8080 || true"
