#!/usr/bin/env python3
"""Compile S4 print match (Concrete). server.zip only on the worker."""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
from concrete import fhe

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.print_xyt import DIM, THRESH_INT, parse_xyt, to_int


@fhe.compiler({"probe": "encrypted", "tmpl": "encrypted"})
def match(probe, tmpl):
    d = probe - tmpl
    return np.sum(d * d) < THRESH_INT


def fixture_ints():
    pinky = to_int(parse_xyt((ROOT / "umbra/fixtures/print/pinky.xyt").read_text()))
    index = to_int(parse_xyt((ROOT / "umbra/fixtures/print/index.xyt").read_text()))
    return np.asarray(pinky, dtype=np.int64), np.asarray(index, dtype=np.int64)


def inputset():
    rng = np.random.default_rng(4)
    rows = []
    pinky, index = fixture_ints()
    rows.append((pinky, pinky))
    rows.append((index, index))
    rows.append((pinky, index))
    rows.append((index, pinky))
    z = np.zeros(DIM, dtype=np.int64)
    rows.append((z, z))
    for _ in range(8):
        a = rng.integers(0, 21, DIM, dtype=np.int64)
        b = rng.integers(0, 21, DIM, dtype=np.int64)
        rows.append((a, a))
        rows.append((a, b))
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts_print")
    args = p.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    print(f"compile print DIM={DIM} THRESH_INT={THRESH_INT}", flush=True)
    circuit = match.compile(inputset())
    srv = out / "server.zip"
    cli = out / "client.zip"
    circuit.server.save(str(srv), via_mlir=True)
    circuit.client.save(str(cli))
    print(f"saved {srv} ({srv.stat().st_size}) {cli} ({cli.stat().st_size})", flush=True)


if __name__ == "__main__":
    main()
