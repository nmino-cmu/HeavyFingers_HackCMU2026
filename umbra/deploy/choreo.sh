#!/bin/bash
# Live container (no docker build/commit): those hang on this Docker+containerd.
set -euo pipefail
source "$HOME/.umbra-vultr.env"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ART="$ROOT/umbra/artifacts/server.zip"
test -f "$ART" || { echo "missing $ART — compile first"; exit 1; }
echo "syncing server.zip + source to worker..."
ssh -o BatchMode=yes "root@$VULTR_WORKER_IP" "mkdir -p /opt/umbra/build /opt/umbra/artifacts && rm -f /opt/umbra/artifacts/client.zip /opt/umbra/artifacts/*.sk /tmp/umbra-artifacts-from-build/client.zip"
COPYFILE_DISABLE=1 tar -C "$ROOT" -czf - --exclude umbra/.env --exclude umbra/artifacts --exclude umbra/__pycache__ umbra \
  | ssh -o BatchMode=yes "root@$VULTR_WORKER_IP" "tar -xzf - -C /opt/umbra/build"
scp -o BatchMode=yes "$ART" "root@$VULTR_WORKER_IP:/opt/umbra/artifacts/server.zip"
ssh -o BatchMode=yes "root@$VULTR_WORKER_IP" bash -s </dev/null <<EOF
set -euo pipefail
ufw allow from 10.20.0.0/24
ufw allow 22/tcp
ufw --force enable
systemctl stop umbra-stub 2>/dev/null || true
pkill -f stub_echo.py || true
docker rm -f umbra-choreo 2>/dev/null || true
docker run -d --name umbra-choreo --restart unless-stopped --network host \\
  -v /opt/umbra/artifacts:/opt/umbra/artifacts:ro \\
  -v /opt/umbra/build/umbra:/opt/umbra-src/umbra:ro \\
  -e PYTHONPATH=/opt/umbra-src \\
  -e UMBRA_FHE_ARTIFACTS=/opt/umbra/artifacts \\
  -e UMBRA_FHE_VPC_IP=\${UMBRA_FHE_VPC_IP:-10.20.0.5} \\
  python:3.11-slim-bookworm \\
  bash -c "apt-get update -qq && apt-get install -y -qq binutils gcc >/dev/null && pip install --no-cache-dir 'concrete-ml==1.7.0' numpy && exec python3 /opt/umbra-src/umbra/worker/choreo_server.py"
sleep 2
docker ps --filter name=umbra-choreo --format '{{.Names}} {{.Status}}'
ss -ltnp | grep 8081 || true
EOF
echo "choreo deploy started (pip may still be running)"
