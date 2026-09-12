#!/usr/bin/env python3
"""Compile S5 floor: Linear(75,10) with bit0 = (v[0] >= 0.5)."""
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

from umbra.fixtures import V_OK, mutant


class TinyS5(nn.Module):
    """bit0 = 20*v[0]-10 (>=0.5 iff v[0]>=0.5); bits 1-9 constant 1 via bias."""

    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(75, 10, bias=True)
        with torch.no_grad():
            self.lin.weight.zero_()
            self.lin.bias.fill_(10.0)
            self.lin.weight[0, 0] = 20.0
            self.lin.bias[0] = -10.0

    def forward(self, x):
        return self.lin(x)


def compile_concrete(out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    model = TinyS5().eval()
    xs = np.asarray([V_OK, mutant("V_LEFT")], dtype=np.float32)
    with torch.no_grad():
        pred = (model(torch.tensor(xs)) >= 0.5).int().tolist()
    if pred[0][0] != 1 or pred[1][0] != 0:
        raise SystemExit(f"tiny cleartext mismatch {pred}")
    quantized = compile_torch_model(model, xs, n_bits=8)
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
