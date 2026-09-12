#!/usr/bin/env python3
"""Four TinyS5 Linear(75,10) circuits, one per public card. Single encrypted input."""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

import numpy as np
import torch
from torch import nn

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.circuits.choreo_floor import bits_from_v
from umbra.fixtures import CARD_LRP, CARD_RLP, CARD_RRI, CARD_RRP, MUTANTS, V_OK, encode_card, mutant

CARDS = {"rrp": CARD_RRP, "lrp": CARD_LRP, "rlp": CARD_RLP, "rri": CARD_RRI}


def _fit_slice(X: np.ndarray, y: np.ndarray):
    xa = np.concatenate([X, np.ones((len(X), 1), dtype=np.float32)], axis=1)
    t = 20.0 * y - 10.0
    w, *_ = np.linalg.lstsq(xa, t, rcond=None)
    return w[:-1].astype(np.float32), np.float32(w[-1])


class TinyCard(nn.Module):
    def __init__(self, w, b):
        super().__init__()
        self.fc = nn.Linear(75, 10)
        with torch.no_grad():
            self.fc.weight.copy_(torch.tensor(w))
            self.fc.bias.copy_(torch.tensor(b))

    def forward(self, x):
        return self.fc(x)


def vectors():
    return [V_OK] + [mutant(m) for m in MUTANTS]


def fit_card(card):
    xs = np.asarray(vectors(), dtype=np.float32)
    ys = np.asarray([bits_from_v(v, card) for v in xs], dtype=np.float32)
    w = np.zeros((10, 75), dtype=np.float32)
    b = np.zeros(10, dtype=np.float32)
    # S5
    if card["hand"] == "right":
        w[0, 0], b[0] = 20.0, -10.0
    else:
        w[0, 0], b[0] = -20.0, 10.0
    w6, b6 = _fit_slice(xs[:, 1:33], ys[:, 1])
    w[1, 1:33], b[1] = w6, b6
    w[2, 33], b[2] = 20.0, -2.0
    if card["side"] == "right":
        w[3, 34], b[3] = 20.0, 0.0
    else:
        w[3, 34], b[3] = -20.0, 0.0
    w9, b9 = _fit_slice(xs[:, 1:67], ys[:, 4])
    w[4, 1:67], b[4] = w9, b9
    w[5, 67], b[5] = 20.0, -8.0
    oh = {"pinky": 68, "index": 69, "thumb": 70}[card["end"]]
    w[6, oh], b[6] = 80.0, -40.0
    w[7, 74], b[7] = 20.0, -10.0
    w[8, 71], w[8, 72], b[8] = -40.0, 40.0, 20.0
    w[9, 73], b[9] = 20.0, -6.0
    model = TinyCard(w, b).eval()
    with torch.no_grad():
        pred = (model(torch.tensor(xs)).numpy() >= 0).astype(np.int32)
    want = ys.astype(np.int32)
    if not np.array_equal(pred, want):
        raise SystemExit(f"{card} miss {(pred != want).sum(axis=0).tolist()}")
    print(f"exact fit {encode_card(card)}")
    return model, xs


def compile_one(name: str, out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    model, xs = fit_card(CARDS[name])
    quantized = compile_torch_model(model, xs, n_bits=8)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved {out_dir}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts-p3")
    p.add_argument("--card", choices=list(CARDS) + ["all"], default="all")
    p.add_argument("--fit-only", action="store_true")
    args = p.parse_args()
    names = list(CARDS) if args.card == "all" else [args.card]
    for name in names:
        if args.fit_only:
            fit_card(CARDS[name])
            continue
        compile_one(name, pathlib.Path(args.out) / name)


if __name__ == "__main__":
    main()
