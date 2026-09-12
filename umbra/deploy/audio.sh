#!/bin/bash
# Host venv on farm-heavy. No docker build / commit.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SSH_HOST="${UMBRA_AUDIO_SSH:-root@104.156.226.53}"
VPC="${UMBRA_FHE_VPC_IP:-10.20.0.7}"
echo "syncing umbra source to $SSH_HOST"
ssh -o BatchMode=yes "$SSH_HOST" "mkdir -p /opt/umbra/build /opt/umbra/artifacts-voice && rm -f /opt/umbra/artifacts-voice/*.sk /opt/umbra/artifacts-voice/*.pt /opt/umbra/artifacts-voice/*.onnx"
COPYFILE_DISABLE=1 tar -C "$ROOT" -czf - --exclude umbra/.env --exclude umbra/artifacts --exclude umbra/artifacts-voice --exclude umbra/artifacts-voice-mac-probe --exclude umbra/__pycache__ umbra \
  | ssh -o BatchMode=yes "$SSH_HOST" "tar -xzf - -C /opt/umbra/build"
echo "compile TinyS2 on farm-heavy"
ssh -o BatchMode=yes "$SSH_HOST" bash -s </dev/null <<'EOF'
set -euo pipefail
export PYTHONPATH=/opt/umbra/build
/opt/umbra/venv311/bin/python /opt/umbra/build/umbra/tools/compile_voice.py --out /opt/umbra/artifacts-voice
test -f /opt/umbra/artifacts-voice/server.zip
test -f /opt/umbra/artifacts-voice/client.zip
EOF
echo "pull client.zip to Mac, strip VM"
mkdir -p "$ROOT/umbra/artifacts-voice"
scp -o BatchMode=yes "$SSH_HOST:/opt/umbra/artifacts-voice/client.zip" "$ROOT/umbra/artifacts-voice/client.zip"
ssh -o BatchMode=yes "$SSH_HOST" "rm -f /opt/umbra/artifacts-voice/client.zip /opt/umbra/artifacts-voice/*.sk"
echo "restart audio_server on VPC $VPC:8083"
ssh -o BatchMode=yes "$SSH_HOST" bash -s </dev/null <<EOF
set -euo pipefail
pkill -f audio_server.py || true
sleep 1
export PYTHONPATH=/opt/umbra/build
export UMBRA_FHE_VPC_IP=$VPC
export UMBRA_AUDIO_PORT=8083
export UMBRA_FHE_ARTIFACTS=/opt/umbra/artifacts-voice
nohup /opt/umbra/venv311/bin/python /opt/umbra/build/umbra/worker/audio_server.py >/var/log/umbra-audio.log 2>&1 &
sleep 2
ss -ltn | grep 8083 || true
curl -sS -m 3 http://$VPC:8083/health || true
find /opt/umbra/artifacts-voice /opt/umbra/build \\( -name '*.pt' -o -name '*.onnx' -o -name client.zip -o -name '*.sk' \\) 2>/dev/null || true
EOF
echo "audio deploy done"
