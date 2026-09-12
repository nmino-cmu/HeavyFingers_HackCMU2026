"""Mac-side FHE client: encrypt v, decrypt bits. Never upload sk."""
from __future__ import annotations

import os
import pathlib
import tempfile

from concrete.ml.deployment import FHEModelClient

from umbra.protocol import pack_request, unpack_request

ARTIFACT_DIR = pathlib.Path(os.environ.get("UMBRA_FHE_ARTIFACTS", "umbra/artifacts"))


class Client:
    """FHEModelClient wrapper with Umbra wire helpers."""

    def __init__(self, artifact_dir: pathlib.Path | str | None = None, key_dir: str | None = None):
        self.artifact_dir = pathlib.Path(artifact_dir or ARTIFACT_DIR)
        self._key_dir = key_dir or os.environ.get("UMBRA_KEY_DIR") or tempfile.mkdtemp(prefix="umbra-keys-")
        self._client = FHEModelClient(path_dir=str(self.artifact_dir), key_dir=self._key_dir)
        self._client.generate_private_and_evaluation_keys()
        self._evk = self._client.get_serialized_evaluation_keys()

    @property
    def evk(self) -> bytes:
        return self._evk

    def quantize_encrypt_serialize(self, v) -> bytes:
        import numpy as np

        x = np.asarray(v, dtype=np.float64).reshape(1, -1)
        return self._client.quantize_encrypt_serialize(x)

    def deserialize_decrypt_dequantize(self, encrypted_result: bytes):
        out = self._client.deserialize_decrypt_dequantize(encrypted_result)
        bits = (out.reshape(-1) >= 0.5).astype(int).tolist()
        return bits

    def pack_eval_body(self, v) -> bytes:
        ct = self.quantize_encrypt_serialize(v)
        return pack_request(self._evk, ct)

    def eval_bits(self, encrypted_result: bytes):
        return self.deserialize_decrypt_dequantize(encrypted_result)


def second_client(artifact_dir: pathlib.Path | str | None = None) -> Client:
    """Independent key material for two-key negative tests."""
    return Client(artifact_dir=artifact_dir, key_dir=tempfile.mkdtemp(prefix="umbra-keys-b-"))
