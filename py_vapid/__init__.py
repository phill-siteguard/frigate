"""Minimal py_vapid stub for tests."""


class _PublicKey:  # pragma: no cover - stub
    def public_bytes(self, encoding, fmt):
        return b""


class Vapid01:  # pragma: no cover - stub
    def __init__(self):
        self.public_key = _PublicKey()

    @classmethod
    def from_file(cls, path):
        return cls()

    def sign(self, claim):
        return {}


class utils:  # pragma: no cover - stub
    @staticmethod
    def b64urlencode(data):
        return ""

