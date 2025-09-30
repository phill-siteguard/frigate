"""Lightweight test stub for the optional sherpa_onnx dependency."""


class OnlineRecognizer:  # pragma: no cover - stub for type checking only
    """Placeholder type used in tests when sherpa_onnx is unavailable."""

    def __init__(self, *args, **kwargs):
        raise RuntimeError(
            "sherpa_onnx is not installed in the test environment."
        )

