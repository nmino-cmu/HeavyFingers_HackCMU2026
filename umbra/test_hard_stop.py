# Tiny check for umbra/hard_stop.py — fails if the halt gate is broken.
import subprocess, sys
from pathlib import Path

r = subprocess.run([sys.executable, "umbra/hard_stop.py"])
assert r.returncode == 0, r
p = Path("umbra/HARD_STOP")
p.write_text("test")
r = subprocess.run([sys.executable, "umbra/hard_stop.py"])
p.unlink()
stopped = Path("umbra/STOPPED.md")
if stopped.exists():
    stopped.unlink()
assert r.returncode == 99, r
print("hard_stop ok")
