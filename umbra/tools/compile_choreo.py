#!/usr/bin/env python3
"""Compile choreography S5–S14 + public card binding (S15)."""
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


class ChoreoP3(nn.Module):
    """Card is clear scalars that scale encrypted heads — no Linear(card)."""

    def __init__(self, hidden: int = 96):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(75, hidden), nn.ReLU())
        self.heads = nn.ModuleList([nn.Linear(hidden, 1) for _ in range(9)])

    def forward(self, x, card):
        e = self.enc(x)
        hand = 2 * card[:, 0:1] - 1
        side = 2 * card[:, 1:2] - 1
        digit = (x[:, 68:71] * card[:, 2:5]).sum(dim=1, keepdim=True)
        parts = [
            self.heads[0](e) * hand,
            self.heads[1](e),
            self.heads[2](e),
            self.heads[3](e) * side,
            self.heads[4](e),
            self.heads[5](e),
            20 * digit - 10,
            self.heads[6](e),
            self.heads[7](e),
            self.heads[8](e),
        ]
        return torch.cat(parts, dim=1)


def training_set():
    cards = [CARD_RRP, CARD_LRP, CARD_RLP, CARD_RRI]
    xs, cs, ys = [], [], []
    vectors = [V_OK] + [mutant(m) for m in MUTANTS]
    for card in cards:
        cvec = encode_card(card)
        for v in vectors:
            xs.append(v)
            cs.append(cvec)
            ys.append(bits_from_v(v, card))
    return np.asarray(xs, dtype=np.float32), np.asarray(cs, dtype=np.float32), np.asarray(ys, dtype=np.float32)


def train_exact(model: ChoreoP3, xs, cs, ys, steps: int = 15000):
    xt = torch.tensor(xs)
    ct = torch.tensor(cs)
    yt = torch.tensor(ys, dtype=torch.float32)
    opt = torch.optim.Adam(model.parameters(), lr=0.03)
    loss_fn = nn.BCEWithLogitsLoss()
    for step in range(steps):
        logits = model(xt, ct)
        loss = loss_fn(logits, yt)
        opt.zero_grad()
        loss.backward()
        opt.step()
        with torch.no_grad():
            pred = (torch.sigmoid(model(xt, ct)) >= 0.5).int()
            if torch.equal(pred, yt.int()):
                print(f"exact fit at step {step}")
                return
    raise SystemExit(f"cleartext mismatch after {steps} steps")


def compile_concrete(out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    xs, cs, ys = training_set()
    model = ChoreoP3().eval()
    train_exact(model, xs, cs, ys)
    quantized = compile_torch_model(
        model,
        (xs, cs),
        n_bits=8,
        inputs_encryption_status=("encrypted", "clear"),
    )
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved artifacts to {out_dir}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts")
    args = p.parse_args()
    compile_concrete(pathlib.Path(args.out))


if __name__ == "__main__":
    main()
