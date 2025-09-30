"""Minimal stub of onnxruntime for test execution."""


class _FakeInput:
    def __init__(self, name: str, shape: tuple[int, ...]):
        self.name = name
        self.shape = shape


class InferenceSession:  # pragma: no cover - stub
    def __init__(self, model_path, providers=None, provider_options=None):
        self._inputs = [_FakeInput("input", (1, 3, 224, 224))]

    def get_inputs(self):
        return self._inputs

    def run(self, output_names, input_feed):
        return []


def get_available_providers():  # pragma: no cover - stub
    return ["CPUExecutionProvider"]

