"""Mac-side OpenFHE print client: encrypt .xyt vector, decrypt match bit. Never upload sk."""
from __future__ import annotations

import hashlib

from openfhe import (
    BINARY,
    CCParamsCKKSRNS,
    DeserializeCiphertextString,
    GenCryptoContext,
    PKESchemeFeature,
    Serialize,
)

from umbra.fixtures import encode_card
from umbra.print_xyt import THRESH
from umbra.protocol import pack_request

DIM = 48


def make_cc():
    params = CCParamsCKKSRNS()
    params.SetMultiplicativeDepth(1)
    params.SetScalingModSize(50)
    params.SetBatchSize(64)
    cc = GenCryptoContext(params)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    return cc


class OpenFHEPrintClient:
    def __init__(self):
        self.cc = make_cc()
        self.keys = self.cc.KeyGen()
        self._sk = self.keys.secretKey
        self.token = hashlib.sha256(Serialize(self.keys.publicKey, BINARY)).digest()
        self._cc_ser = Serialize(self.cc, BINARY)

    def encrypt(self, vec) -> bytes:
        pt = self.cc.MakeCKKSPackedPlaintext([float(x) for x in vec])
        return Serialize(self.cc.Encrypt(self.keys.publicKey, pt), BINARY)

    def pack_enroll(self, vec) -> bytes:
        return pack_request(self.token + self._cc_ser, self.encrypt(vec))

    def pack_print(self, vec, card) -> bytes:
        return pack_request(self.token, self.encrypt(vec), encode_card(card))

    def decrypt_bit(self, encrypted_diff: bytes) -> int:
        ct = DeserializeCiphertextString(encrypted_diff, BINARY)
        pt = self.cc.Decrypt(self._sk, ct)
        pt.SetLength(DIM)
        vals = list(pt.GetRealPackedValue())
        return int(sum(x * x for x in vals) < THRESH)


def second_openfhe_print_client() -> OpenFHEPrintClient:
    return OpenFHEPrintClient()


def _self_check():
    # ponytail: fails if EvalSub match bit flips
    from umbra.print_xyt import match_bit

    a = [0.2] * DIM
    b = [0.9] * DIM
    c = OpenFHEPrintClient()
    d0 = c.cc.EvalSub(
        c.cc.Encrypt(c.keys.publicKey, c.cc.MakeCKKSPackedPlaintext(a)),
        c.cc.Encrypt(c.keys.publicKey, c.cc.MakeCKKSPackedPlaintext(a)),
    )
    d1 = c.cc.EvalSub(
        c.cc.Encrypt(c.keys.publicKey, c.cc.MakeCKKSPackedPlaintext(a)),
        c.cc.Encrypt(c.keys.publicKey, c.cc.MakeCKKSPackedPlaintext(b)),
    )
    assert c.decrypt_bit(Serialize(d0, BINARY)) == 1
    assert c.decrypt_bit(Serialize(d1, BINARY)) == 0
    assert match_bit(a, a) == 1 and match_bit(a, b) == 0
    print("OPENFHE_CLIENT_SELF_CHECK_OK")


if __name__ == "__main__":
    _self_check()
