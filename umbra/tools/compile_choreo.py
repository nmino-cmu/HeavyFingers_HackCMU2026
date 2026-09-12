#!/usr/bin/env python3
"""Compile TinyChoreo with concrete.fhe: encrypted v, clear public card. No Adam."""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

import numpy as np
import torch

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.circuits.tiny_choreo import TinyChoreo
from umbra.fixtures import (
    CARD_LRP,
    CARD_RLP,
    CARD_RRI,
    CARD_RRP,
    MUTANTS,
    V_OK,
    encode_card,
    mutant,
    reference,
)

CARDS = [CARD_RRP, CARD_LRP, CARD_RLP, CARD_RRI]
SCALE = 100
THRESH = 50


def quant_v(v) -> np.ndarray:
    return np.rint(np.asarray(v, dtype=np.float64) * SCALE).astype(np.int64)


def quant_card(card) -> np.ndarray:
    return np.rint(np.asarray(encode_card(card), dtype=np.float64)).astype(np.int64)


def weight_bias():
    m = TinyChoreo().eval()
    w = np.rint(m.lin.weight.detach().numpy().T).astype(np.int64)  # (75, 10)
    b = np.rint(m.lin.bias.detach().numpy() * SCALE).astype(np.int64)
    return w, b


def inputset():
    rows = []
    for card in CARDS:
        cq = quant_card(card)
        for v in [V_OK] + [mutant(m) for m in MUTANTS]:
            rows.append((quant_v(v), cq))
    return rows


def bits_from_y(y) -> list:
    return (np.asarray(y).reshape(-1) >= THRESH).astype(int).tolist()


def check_integer():
    w, b = weight_bias()
    bad = 0
    for card in CARDS:
        cq = quant_card(card)
        for v in [V_OK] + [mutant(m) for m in MUTANTS]:
            x = quant_v(v)
            y = x @ w + b
            y = y.astype(np.int64).copy()
            y[0] = y[0] * cq[0] + y[0] * cq[0] - y[0]
            y[3] = y[3] * cq[1] + y[3] * cq[1] - y[3]
            y[6] = 20 * (x[68] * cq[2] + x[69] * cq[3] + x[70] * cq[4]) - 1000
            got = bits_from_y(y)
            want = reference(v, card)
            if got != want:
                bad += 1
                print("int mismatch", got, want)
    if bad:
        raise SystemExit(f"integer cleartext mismatches {bad}")
    print(f"integer cleartext ok rows={len(CARDS) * (1 + len(MUTANTS))}")


def make_circuit():
    from concrete import fhe

    w, b = weight_bias()

    @fhe.compiler({"x": "encrypted", "card": "clear"})
    def choreo(x, card):
        y = x @ w + b
        s5 = y[0] * card[0] + y[0] * card[0] - y[0]
        s8 = y[3] * card[1] + y[3] * card[1] - y[3]
        s11 = 20 * (x[68] * card[2] + x[69] * card[3] + x[70] * card[4]) - 1000
        return fhe.array([s5, y[1], y[2], s8, y[4], y[5], s11, y[7], y[8], y[9]])

    return choreo


def compile_concrete(out_dir: pathlib.Path):
    from concrete import fhe

    check_integer()
    choreo = make_circuit()
    print("compiling concrete.fhe TinyChoreo...")
    circuit = choreo.compile(inputset())
    print("compiled pbs", circuit.programmable_bootstrap_count)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    circuit.server.save(out_dir / "server.zip", via_mlir=True)
    circuit.client.save(out_dir / "client.zip")
    np.savez(out_dir / "qparams.npz", scale=SCALE, thresh=THRESH)
    print(f"saved artifacts to {out_dir}")
    return circuit


def probe_tiny():
    """Mac FHE probe once: Tiny Linear S5, clear public hand. Not the demo host."""
    from concrete import fhe

    @fhe.compiler({"x0": "encrypted", "hand": "clear"})
    def s5(x0, hand):
        d = x0 - 50
        return d * hand + d * hand - d

    circuit = s5.compile([(91, 1), (8, 1), (91, 0), (8, 0)])
    circuit.keygen()
    enc = circuit.encrypt(91, 1)
    same_ct = enc[0]
    d1 = circuit.decrypt(circuit.run(same_ct, 1))
    d0 = circuit.decrypt(circuit.run(same_ct, 0))
    if d1 < 0 or d0 >= 0:
        raise SystemExit(f"probe bits wrong d1={d1} d0={d0}")
    print("MAC_FHE_PROBE=ok", "same_ct", "hand1", d1, "hand0", d0, "pbs", circuit.programmable_bootstrap_count)


def probe_full(circuit):
    circuit.keygen()
    x = quant_v(V_OK)
    enc = circuit.encrypt(x, quant_card(CARD_RRP))
    ct = enc[0]
    y_rrp = circuit.decrypt(circuit.run(ct, quant_card(CARD_RRP)))
    y_lrp = circuit.decrypt(circuit.run(ct, quant_card(CARD_LRP)))
    print("full RRP", bits_from_y(y_rrp), "LRP", bits_from_y(y_lrp))
    if bits_from_y(y_rrp) != reference(V_OK, CARD_RRP):
        raise SystemExit("full probe RRP mismatch")
    if bits_from_y(y_lrp)[0] != 0:
        raise SystemExit("full probe LRP S5 not 0")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts-p3")
    p.add_argument("--probe", action="store_true", help="Mac Tiny Linear probe only")
    p.add_argument("--check-only", action="store_true")
    p.add_argument("--full-probe", action="store_true")
    args = p.parse_args()
    if args.check_only:
        check_integer()
        return
    if args.probe:
        probe_tiny()
        return
    circuit = compile_concrete(pathlib.Path(args.out))
    if args.full_probe:
        probe_full(circuit)


if __name__ == "__main__":
    main()
