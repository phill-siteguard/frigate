"""Minimal ONVIF client stub for tests."""


class ONVIFError(Exception):
    pass


class ONVIFService:  # pragma: no cover - stub
    def __init__(self):
        self.xaddr = ""

    async def GetProfiles(self):
        return []

    def create_type(self, name):
        return type("Request", (), {})()


class ONVIFCamera:  # pragma: no cover - stub
    def __init__(self, *args, **kwargs):
        pass

    async def update_xaddrs(self):
        return None

    async def create_media_service(self):
        return ONVIFService()

    async def create_ptz_service(self):
        return ONVIFService()

    async def create_imaging_service(self):
        return ONVIFService()

    def get_definition(self, name):
        return {}

