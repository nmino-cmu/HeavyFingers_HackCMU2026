#!/bin/bash
# Fail if live spawn law is not Grok 4.6 xhigh FAST. Zero-token monitor helper.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
SLUG='cursor-grok-4.6-xhigh-fast'
FAIL=0

LIVE=(
  .cursor/rules/umbra-fast-mode.mdc
  docs/superpowers/plans/2026-09-12-umbra-ORCHESTRATOR.md
  docs/superpowers/plans/2026-09-12-umbra-RULES.md
  docs/superpowers/plans/2026-09-12-umbra-PHASES.md
  umbra/PAUSE.md
  docs/superpowers/plans/2026-09-12-umbra-P0-infra.md
  docs/superpowers/plans/2026-09-12-umbra-P1-orch.md
  docs/superpowers/plans/2026-09-12-umbra-P2-floor-fhe.md
  docs/superpowers/plans/2026-09-12-umbra-P3-choreo.md
  docs/superpowers/plans/2026-09-12-umbra-P4-s1-s19.md
  docs/superpowers/plans/2026-09-12-umbra-P5-print.md
  docs/superpowers/plans/2026-09-12-umbra-P6-voice-digit.md
  docs/superpowers/plans/2026-09-12-umbra-P7-face.md
  docs/superpowers/plans/2026-09-12-umbra-P8-bid.md
  docs/superpowers/plans/2026-09-12-umbra-P9-hops-ui.md
)

for f in "${LIVE[@]}"; do
  # main dropped plan files after submit; skip ghosts so this loop does not false-alarm
  if [ ! -f "$f" ]; then
    continue
  fi
  if ! grep -q "$SLUG" "$f"; then
    echo "MISSING $SLUG in $f"
    FAIL=1
  fi
done

# Composer as a spawn target in live law (not "never Composer")
hits="$(
  grep -n 'composer-2\.5' "${LIVE[@]}" 2>/dev/null \
    | grep -v 'Never spawn Composer' \
    | grep -v 'Never Composer' \
    | grep -v 'not grok' \
    | grep -v 'use composer' \
    || true
)"
if [ -n "$hits" ]; then
  echo "COMPOSER STILL A SPAWN TARGET:"
  echo "$hits"
  FAIL=1
fi

# Fable as default compile builder (must say only-if / stuck)
fable_hits="$(
  grep -n 'Fable 5.1 Task' \
    docs/superpowers/plans/2026-09-12-umbra-P3-choreo.md \
    docs/superpowers/plans/2026-09-12-umbra-P5-print.md \
    docs/superpowers/plans/2026-09-12-umbra-P6-voice-digit.md \
    docs/superpowers/plans/2026-09-12-umbra-P7-face.md \
    2>/dev/null \
    | grep -v stuck \
    | grep -v 'only if' \
    || true
)"
if [ -n "$fable_hits" ]; then
  echo "FABLE AS DEFAULT BUILDER:"
  echo "$fable_hits"
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  exit 1
fi
echo "FAST_OK $SLUG"
