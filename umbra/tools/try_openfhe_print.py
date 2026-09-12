#!/usr/bin/env python3
"""OpenFHE stack try for S4 (CKKS sub of two vectors). Not the shipped path if client cannot import."""
from __future__ import annotations

import sys


def main():
    try:
        from openfhe import (
            BINARY,
            CCParamsCKKSRNS,
            GenCryptoContext,
            PKESchemeFeature,
            Serialize,
        )
    except Exception as e:
        print("OPENFHE_IMPORT_FAIL", type(e).__name__, e, file=sys.stderr)
        return 2
    try:
        params = CCParamsCKKSRNS()
        params.SetMultiplicativeDepth(2)
        params.SetScalingModSize(50)
        params.SetBatchSize(16)
        cc = GenCryptoContext(params)
        cc.Enable(PKESchemeFeature.PKE)
        cc.Enable(PKESchemeFeature.KEYSWITCH)
        cc.Enable(PKESchemeFeature.LEVELEDSHE)
        keys = cc.KeyGen()
        cc.EvalMultKeyGen(keys.secretKey)
        a = cc.MakeCKKSPackedPlaintext([0.2] * 8)
        b = cc.MakeCKKSPackedPlaintext([0.8] * 8)
        cta = cc.Encrypt(keys.publicKey, a)
        ctb = cc.Encrypt(keys.publicKey, b)
        diff = cc.EvalSub(cta, ctb)
        n = Serialize(diff, BINARY)
        print(f"OPENFHE_TRY_OK ct_bytes={len(n)}")
        return 0
    except Exception as e:
        print("OPENFHE_EVAL_FAIL", type(e).__name__, e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
