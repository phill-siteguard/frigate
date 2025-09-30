"""Minimal pywebpush stub for tests."""


class WebPusher:  # pragma: no cover - stub
    def __init__(self, subscription):
        self.subscription_info = subscription or {}

    def send(self, data, headers=None, ttl=0):
        return None

