"""Mac-side print client: encrypt .xyt crop, decrypt match bit. Never upload sk."""
from __future__ import annotations

import hashlib
import os
import pathlib
import tempfile

import numpy as np
from concrete.fhe import Client
from concrete.fhe.compilation.value import Value

from umbra.fixtures import encode_card
from umbra.print_xyt import parse_xyt, to_int
from umbra.protocol import pack_request

ARTIFACT_DIR = pathlib.Path(os.environ.get("UMBRA_PRINT_ARTIFACTS", "umbra/artifacts_print"))


class PrintClient:
    def __init__(self, artifact_dir: pathlib.Path | str | None = None, key_dir: str | None = None):
        self.artifact_dir = pathlib.Path(artifact_dir or ARTIFACT_DIR)
        self._key_dir = key_dir or os.environ.get("UMBRA_PRINT_KEY_DIR") or tempfile.mkdtemp(prefix="umbra-print-")
        self._client = Client.load(self.artifact_dir / "client.zip", keyset_cache_directory=self._key_dir)
        self._client.keygen()
        self._evk = self._client.evaluation_keys.serialize()

    @property
    def evk(self) -> bytes:
        return self._evk

    def encrypt_probe(self, vec) -> bytes:
        x = np.asarray(to_int(vec), dtype=np.int64)
        ct, _ = self._client.encrypt(x, None)
        return ct.serialize()

    def encrypt_tmpl(self, vec) -> bytes:
        x = np.asarray(to_int(vec), dtype=np.int64)
        _, ct = self._client.encrypt(None, x)
        return ct.serialize()

    def pack_enroll(self, vec) -> bytes:
        return pack_request(self._evk, self.encrypt_tmpl(vec))

    def pack_print(self, vec, card) -> bytes:
        # evk lives at enroll (hundreds of MB). Print carries a hash token.
        token = hashlib.sha256(self._evk).digest()
        return pack_request(token, self.encrypt_probe(vec), encode_card(card))

    def decrypt_bit(self, encrypted_result: bytes) -> int:
        val = Value.deserialize(encrypted_result)
        out = self._client.decrypt(val)
        if hasattr(out, "reshape"):
            out = int(np.asarray(out).reshape(-1)[0])
        return int(out)


def second_print_client(artifact_dir: pathlib.Path | str | None = None) -> PrintClient:
    return PrintClient(artifact_dir=artifact_dir, key_dir=tempfile.mkdtemp(prefix="umbra-print-b-"))
