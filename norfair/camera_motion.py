"""Minimal stub of norfair.camera_motion for tests."""


class HomographyTransformationGetter:  # pragma: no cover - stub
    pass


class TranslationTransformationGetter:  # pragma: no cover - stub
    pass


class _Transform:  # pragma: no cover - stub
    def rel_to_abs(self, points):
        return points


class MotionEstimator:  # pragma: no cover - stub
    def __init__(self, transformations_getter=None, min_distance=None, max_points=None):
        self.transformations_getter = transformations_getter

    def update(self, frame, mask):
        return _Transform()

