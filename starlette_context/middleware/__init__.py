"""Minimal ContextMiddleware stub."""


class ContextMiddleware:  # pragma: no cover - stub
    def __init__(self, app, plugins=None, **kwargs):
        self.app = app
        self.plugins = plugins or []

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

