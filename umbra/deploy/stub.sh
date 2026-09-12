#!/bin/bash
set -euo pipefail
source "$HOME/.umbra-vultr.env"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ssh -o BatchMode=yes "root@$VULTR_WORKER_IP" "mkdir -p /opt/umbra; ufw allow from 10.20.0.0/24; ufw --force enable"
scp "$ROOT/umbra/worker/stub_echo.py" "root@$VULTR_WORKER_IP:/opt/umbra/stub_echo.py"
ssh -o BatchMode=yes "root@$VULTR_WORKER_IP" "systemctl stop umbra-fhe-smoke 2>/dev/null || true
pkill -f stub_echo.py || true
pkill -f 'http.server 8081' || true
UMBRA_FHE_VPC_IP=$UMBRA_FHE_VPC_IP nohup python3 /opt/umbra/stub_echo.py >/tmp/stub.log 2>&1 &
sleep 1
ss -ltnp | grep 8081 || true"
