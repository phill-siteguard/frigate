"""Minimal faster_whisper stub for tests."""


class _Info:
    def __init__(self):
        self.language = "en"
        self.language_probability = 1.0


class WhisperModel:  # pragma: no cover - stub
    def __init__(self, *args, **kwargs):
        pass

    def transcribe(self, *args, **kwargs):
        return [], _Info()


class BatchedInferencePipeline:  # pragma: no cover - stub
    def __init__(self, model=None):
        self.model = model

    def transcribe(self, *args, **kwargs):
        return [], _Info()

