"""Hand-written Tiny Linear choreography: S5–S14 + public card (S15). No Adam."""
from __future__ import annotations

import numpy as np
import torch
from torch import nn

from umbra.fixtures import CARD_RRP, MUTANTS, V_OK, mutant, reference


def _ridge_row(xs: np.ndarray, ys: np.ndarray, ridge: float = 1e-2) -> np.ndarray:
    a = xs.T @ xs + ridge * np.eye(xs.shape[1])
    return np.linalg.solve(a, xs.T @ ys).astype(np.float32)


def _s6_s9_weights():
    rows = [V_OK] + [mutant(m) for m in MUTANTS]
    xs = np.asarray(rows, dtype=np.float64)
    y6 = np.array([1.0 if reference(v, CARD_RRP)[1] == 1 else -1.0 for v in rows])
    y9 = np.array([1.0 if reference(v, CARD_RRP)[4] == 1 else -1.0 for v in rows])
    return _ridge_row(xs, y6), _ridge_row(xs, y9)


class TinyS5Card(nn.Module):
    """Mac FHE probe: bit0 = (20*v[0]-10)*hand. One output."""

    def forward(self, x, card):
        hand = 2 * card[:, 0:1] - 1
        return (20 * x[:, 0:1] - 10) * hand


class TinyChoreo(nn.Module):
    """Linear(75,10) * Linear(5,10) card scales; S11 is digit·end."""

    def __init__(self):
        super().__init__()
        w6, w9 = _s6_s9_weights()
        self.lin = nn.Linear(75, 10, bias=True)
        self.card_lin = nn.Linear(5, 10, bias=True)
        self.s11_expand = nn.Linear(1, 10, bias=True)
        with torch.no_grad():
            self.lin.weight.zero_()
            self.lin.bias.zero_()
            self.lin.weight[0, 0] = 20.0
            self.lin.bias[0] = -10.0
            self.lin.weight[1] = torch.from_numpy(20.0 * w6)
            self.lin.weight[4] = torch.from_numpy(20.0 * w9)
            self.lin.weight[2, 33] = 20.0
            self.lin.bias[2] = -2.0
            self.lin.weight[3, 34] = 50.0
            self.lin.weight[5, 67] = 20.0
            self.lin.bias[5] = -8.0
            self.lin.weight[7, 74] = 20.0
            self.lin.bias[7] = -10.0
            self.lin.weight[8, 72] = 20.0
            self.lin.weight[8, 71] = -20.0
            self.lin.bias[8] = 10.0
            self.lin.weight[9, 73] = 20.0
            self.lin.bias[9] = -6.0
            # card: S5 *hand, S8 *side, others *1, S11 *0 (filled by s11_expand)
            self.card_lin.weight.zero_()
            self.card_lin.bias.fill_(1.0)
            self.card_lin.weight[0, 0] = 2.0
            self.card_lin.bias[0] = -1.0
            self.card_lin.weight[3, 1] = 2.0
            self.card_lin.bias[3] = -1.0
            self.card_lin.bias[6] = 0.0
            self.s11_expand.weight.zero_()
            self.s11_expand.bias.zero_()
            self.s11_expand.weight[6, 0] = 20.0
            self.s11_expand.bias[6] = -10.0

    def forward(self, x, card):
        y = self.lin(x) * self.card_lin(card)
        prod = (x[:, 68:71] * card[:, 2:5]).sum(dim=1, keepdim=True)
        return y + self.s11_expand(prod)


def logits_to_bits(logits) -> list:
    return (logits.reshape(-1) >= 0.5).to(torch.int64).tolist()
