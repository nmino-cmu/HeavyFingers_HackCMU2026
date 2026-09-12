"""Mac-side FHE client: encrypt v, decrypt bits. Never upload sk."""
from __future__ import annotations

import os
import pathlib
import tempfile

import numpy as np

from umbra.fixtures import encode_card
from umbra.protocol import pack_request, unpack_request

ARTIFACT_DIR = pathlib.Path(os.environ.get("UMBRA_FHE_ARTIFACTS", "umbra/artifacts"))


def _is_clear_card(artifact_dir: pathlib.Path) -> bool:
    return (artifact_dir / "qparams.npz").is_file()


class Client:
    """FHE wrapper. P2 = Concrete-ML TinyS5; P3 = concrete.fhe + public card."""

    def __init__(self, artifact_dir: pathlib.Path | str | None = None, key_dir: str | None = None):
        self.artifact_dir = pathlib.Path(artifact_dir or ARTIFACT_DIR)
        self._key_dir = key_dir or os.environ.get("UMBRA_KEY_DIR") or tempfile.mkdtemp(prefix="umbra-keys-")
        self._kind = "fhe" if _is_clear_card(self.artifact_dir) else "cml"
        if self._kind == "fhe":
            from concrete import fhe

            q = np.load(self.artifact_dir / "qparams.npz")
            self._scale = int(q["scale"])
            self._thresh = int(q["thresh"])
            self._fhe = fhe.Client.load(str(self.artifact_dir / "client.zip"), self._key_dir)
            self._fhe.keygen()
            self._evk = self._fhe.evaluation_keys.serialize()
            self._client = None
        else:
            from concrete.ml.deployment import FHEModelClient

            self._fhe = None
            self._client = FHEModelClient(path_dir=str(self.artifact_dir), key_dir=self._key_dir)
            self._client.generate_private_and_evaluation_keys()
            self._evk = self._client.get_serialized_evaluation_keys()
            self._scale = 1
            self._thresh = 1

    @property
    def evk(self) -> bytes:
        return self._evk

    def quantize_encrypt_serialize(self, v, card=None) -> bytes:
        if self._kind == "fhe":
            x = np.rint(np.asarray(v, dtype=np.float64) * self._scale).astype(np.int64)
            dummy = np.ones(5, dtype=np.int64)
            enc = self._fhe.encrypt(x, dummy)
            return enc[0].serialize()
        x = np.asarray(v, dtype=np.float64).reshape(1, -1)
        if card is None:
            return self._client.quantize_encrypt_serialize(x)
        c = np.asarray(encode_card(card), dtype=np.float64).reshape(1, -1)
        return self._client.quantize_encrypt_serialize(x, c)

    def deserialize_decrypt_dequantize(self, encrypted_result: bytes):
        if self._kind == "fhe":
            from concrete.fhe import Value

            y = self._fhe.decrypt(Value.deserialize(encrypted_result))
            return (np.asarray(y).reshape(-1) >= self._thresh).astype(int).tolist()
        out = self._client.deserialize_decrypt_dequantize(encrypted_result)
        return (out.reshape(-1) >= 0.5).astype(int).tolist()

    def pack_eval_body(self, v, card) -> bytes:
        ct = self.quantize_encrypt_serialize(v)
        return self.pack_eval_body_from_ct(ct, card)

    def clear_card_array(self, card):
        return np.asarray(encode_card(card), dtype=np.float64).reshape(1, -1)

    def pack_eval_body_from_ct(self, ct: bytes, card) -> bytes:
        return pack_request(self._evk, ct, encode_card(card))

    def eval_bits(self, encrypted_result: bytes):
        return self.deserialize_decrypt_dequantize(encrypted_result)


def second_client(artifact_dir: pathlib.Path | str | None = None) -> Client:
    """Independent key material for two-key negative tests."""
    return Client(artifact_dir=artifact_dir, key_dir=tempfile.mkdtemp(prefix="umbra-keys-b-"))
