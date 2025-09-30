"""Utility helpers for Frigate API modules."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Tuple


def inject_camera_meta(data: Any, frigate_config) -> Tuple[bool, bool]:
    """Inject camera meta information into response payloads.

    Args:
        data: Arbitrary JSON-serialisable data structure containing event objects.
        frigate_config: The active :class:`~frigate.config.FrigateConfig` instance.

    Returns:
        A tuple ``(injected, found_camera)`` indicating whether a ``camera_meta``
        field was inserted and whether any ``camera`` fields were encountered
        during traversal respectively.
    """

    injected = False
    found_camera = False

    def _inject(obj: Any) -> None:
        nonlocal injected, found_camera

        if isinstance(obj, dict):
            if "camera" in obj:
                found_camera = True

                if "camera_meta" not in obj:
                    camera_name = obj.get("camera")
                    meta = {}

                    try:
                        camera_config = None
                        if frigate_config is not None:
                            camera_config = frigate_config.cameras.get(camera_name)

                        if (
                            camera_config is not None
                            and getattr(camera_config, "meta", None) is not None
                        ):
                            meta = camera_config.meta or {}
                    except Exception:
                        meta = {}

                    obj["camera_meta"] = meta
                    injected = True

            for value in obj.values():
                _inject(value)

        elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray)):
            for item in obj:
                _inject(item)

    _inject(data)

    return injected, found_camera

