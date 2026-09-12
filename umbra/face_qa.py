"""On-Mac Vision face QA + align. Crops stay here; Vultr only sees ciphertext."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from umbra.enroll_extract import FACE_N, crop_grid, image_to_grid, prep_face

HERE = Path(__file__).resolve().parent
BIN = HERE / "bin" / "vision_qa"
SRC = HERE / "tools" / "vision_qa.swift"

# Vision: +yaw = subject turned their own left. Preview is CSS-mirrored; hints are YOUR left/right.
# Only reject a side shot when yaw is clearly the other way. Missing yaw does not block.
POSES = {
    "front": lambda yaw: True,
    "left": lambda yaw: yaw >= -0.18,
    "right": lambda yaw: yaw <= 0.18,
}


def ensure_bin() -> Path:
    if sys.platform != "darwin":
        raise RuntimeError("vision_qa is macOS-only")
    if BIN.is_file() and BIN.stat().st_mtime >= SRC.stat().st_mtime:
        return BIN
    BIN.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["swiftc", "-O", "-o", str(BIN), str(SRC)])
    return BIN


def inspect_paths(paths: list[str]) -> list[dict]:
    if not paths:
        return []
    if sys.platform != "darwin":
        return [{"path": p, "w": 0, "h": 0, "faces": [], "hands": []} for p in paths]
    r = subprocess.run([str(ensure_bin()), *paths], capture_output=True, timeout=60)
    if r.returncode != 0 or not r.stdout:
        return [{"path": p, "w": 0, "h": 0, "faces": [], "hands": []} for p in paths]
    return json.loads(r.stdout.decode())


def inspect_bytes(data: bytes) -> dict:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "f.jpg"
        if data[:2] == b"\xff\xd8":
            p.write_bytes(data)
        else:
            raw = Path(td) / "in.bin"
            raw.write_bytes(data)
            subprocess.run(
                ["sips", "-s", "format", "jpeg", str(raw), "--out", str(p)],
                capture_output=True,
            )
        rows = inspect_paths([str(p)])
    return rows[0] if rows else {"faces": [], "hands": [], "w": 0, "h": 0}


def _largest(faces: list[dict]) -> dict | None:
    if not faces:
        return None
    return max(faces, key=lambda f: float(f.get("w", 0)) * float(f.get("h", 0)))


def blur_var(grid: list[float]) -> float:
    n = FACE_N
    acc = 0.0
    k = 0
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            i = y * n + x
            lap = 4 * grid[i] - grid[i - 1] - grid[i + 1] - grid[i - n] - grid[i + n]
            acc += lap * lap
            k += 1
    return acc / k if k else 0.0


def qa_still(data: bytes, pose: str = "front") -> dict:
    """ok iff Vision found a face (green oval). A side pose also fails when yaw is clearly the other way.

    No size/center/blur/light gates: those blocked enroll. Pose is advisory; snap saves regardless.
    """
    pose = pose if pose in POSES else "front"
    if sys.platform != "darwin":
        # ponytail: oval lock is in the browser; Vision is Mac-only
        return {"ok": True, "reason": "", "pose": pose, "face": {"x": 0.15, "y": 0.1, "w": 0.7, "h": 0.8, "yaw": 0.0}, "yaw": 0.0}
    face = _largest(inspect_bytes(data).get("faces") or [])
    yaw = float(face.get("yaw") or 0) if face else 0.0
    reason = "" if face else "no face — fill the oval"
    # ponytail: only refuse a side when Vision is sure it's the other way; POSES["front"] never refuses
    if face and abs(yaw) >= 0.22 and not POSES[pose](yaw):
        reason = "other way — turn YOUR " + pose + " and hold"
    return {"ok": not reason, "reason": reason, "pose": pose, "face": face, "yaw": yaw}


def grid_for_enroll(data: bytes) -> list[float]:
    """Align if Vision finds a face; else full-frame (synthetic tests)."""
    if os.environ.get("UMBRA_SKIP_ALIGN") == "1":
        return image_to_grid(data)
    try:
        face = _largest((inspect_bytes(data).get("faces") or []))
        if face and float(face["w"]) >= 0.12:
            return prep_face(crop_grid(data, face))
    except Exception:
        pass
    return prep_face(image_to_grid(data))
