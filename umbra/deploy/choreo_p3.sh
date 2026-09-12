#!/bin/bash
# farm-a only. Do not touch live umbra-choreo / 10.20.0.5.
set -euo pipefail
source "$HOME/.umbra-vultr.env"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FARM_A="${UMBRA_FARM_A_IP:-207.246.94.252}"
FARM_VPC="${UMBRA_FARM_A_VPC_IP:-10.20.0.4}"
echo "syncing source to farm-a $FARM_A (no .env, no client.zip)..."
ssh -o BatchMode=yes "root@$FARM_A" "mkdir -p /opt/umbra/p3 && rm -f /opt/umbra/p3/client.zip /opt/umbra/p3/*.sk /opt/umbra/p3/artifacts/client.zip"
COPYFILE_DISABLE=1 tar -C "$ROOT" -czf - \
  --exclude umbra/.env --exclude umbra/artifacts --exclude umbra/artifacts-p3 \
  --exclude umbra/artifacts-p3-mac --exclude umbra/__pycache__ \
  --exclude 'umbra/**/__pycache__' umbra \
  | ssh -o BatchMode=yes "root@$FARM_A" "rm -rf /opt/umbra/p3/src && mkdir -p /opt/umbra/p3/src && tar -xzf - -C /opt/umbra/p3/src"
ssh -o BatchMode=yes "root@$FARM_A" bash -s </dev/null <<EOF
set -euo pipefail
ufw allow from 10.20.0.0/24
ufw allow 22/tcp
ufw --force enable
docker exec umbra-p3 bash -c 'rm -f /opt/umbra/src/umbra/artifacts-p3/client.zip /opt/umbra/artifacts/client.zip'
docker exec -e PYTHONPATH=/opt/umbra/src umbra-p3 python3 /opt/umbra/src/umbra/tools/compile_choreo.py --out /opt/umbra/artifacts
ls -la /opt/umbra/p3/artifacts
EOF
echo "pulling client.zip to Mac (never leave it on the VM)..."
mkdir -p "$ROOT/umbra/artifacts-p3"
scp -o BatchMode=yes "root@$FARM_A:/opt/umbra/p3/artifacts/client.zip" "$ROOT/umbra/artifacts-p3/client.zip"
scp -o BatchMode=yes "root@$FARM_A:/opt/umbra/p3/artifacts/qparams.npz" "$ROOT/umbra/artifacts-p3/qparams.npz"
ssh -o BatchMode=yes "root@$FARM_A" "rm -f /opt/umbra/p3/artifacts/client.zip /opt/umbra/p3/client.zip; find /opt/umbra /tmp -name client.zip -o -name '*.sk' | head"
ssh -o BatchMode=yes "root@$FARM_A" bash -s </dev/null <<EOF
set -euo pipefail
docker exec umbra-p3 bash -c 'pkill -f choreo_server.py || true'
docker exec -d \
  -e PYTHONPATH=/opt/umbra/src \
  -e UMBRA_FHE_ARTIFACTS=/opt/umbra/artifacts \
  -e UMBRA_FHE_VPC_IP=$FARM_VPC \
  -e UMBRA_FHE_PORT=8081 \
  umbra-p3 python3 /opt/umbra/src/umbra/worker/choreo_server.py
sleep 2
docker exec umbra-p3 ss -ltnp | grep 8081 || true
EOF
echo "farm-a P3 worker started on $FARM_VPC:8081"
