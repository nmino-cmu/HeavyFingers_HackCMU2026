#!/bin/bash
# Compile on farm-fast (not live choreo). No docker build/commit.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PRINT_IP="${UMBRA_PRINT_PUBLIC_IP:-45.32.5.249}"
PRINT_VPC="${UMBRA_PRINT_VPC_IP:-10.20.0.6}"
echo "syncing print source to farm-fast..."
ssh -o BatchMode=yes "root@$PRINT_IP" "mkdir -p /opt/umbra/build /opt/umbra/print/artifacts /opt/umbra/print/templates && rm -f /opt/umbra/print/artifacts/client.zip /opt/umbra/print/artifacts/*.sk"
COPYFILE_DISABLE=1 tar -C "$ROOT" -czf - --exclude umbra/.env --exclude umbra/artifacts --exclude umbra/artifacts_print --exclude umbra/__pycache__ umbra \
  | ssh -o BatchMode=yes "root@$PRINT_IP" "tar -xzf - -C /opt/umbra/build"
ssh -o BatchMode=yes "root@$PRINT_IP" bash -s </dev/null <<EOF
set -euo pipefail
ufw allow 22/tcp
ufw allow from 10.20.0.0/24
ufw --force enable
export PYTHONPATH=/opt/umbra/build
/opt/umbra/venv/bin/python /opt/umbra/build/umbra/tools/compile_print.py --out /opt/umbra/print/artifacts
EOF
mkdir -p "$ROOT/umbra/artifacts_print"
scp -o BatchMode=yes "root@$PRINT_IP:/opt/umbra/print/artifacts/client.zip" "$ROOT/umbra/artifacts_print/client.zip"
ssh -o BatchMode=yes "root@$PRINT_IP" bash -s </dev/null <<EOF
set -euo pipefail
rm -f /opt/umbra/print/artifacts/client.zip /opt/umbra/print/artifacts/*.sk
pkill -f print_server.py || true
export UMBRA_PRINT_VPC_IP=${PRINT_VPC}
export UMBRA_PRINT_PORT=8082
export UMBRA_PRINT_ARTIFACTS=/opt/umbra/print/artifacts
export UMBRA_PRINT_STORE=/opt/umbra/print/templates
export PYTHONPATH=/opt/umbra/build
nohup /opt/umbra/venv/bin/python /opt/umbra/build/umbra/worker/print_server.py >/var/log/umbra-print.log 2>&1 &
sleep 1
ss -ltnp | grep 8082 || true
test ! -f /opt/umbra/print/artifacts/client.zip
EOF
echo "print deploy started; client.zip on Mac only"
