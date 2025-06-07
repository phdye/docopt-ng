"""Minimal pathlib backport for old Python.

This module provides a small subset of :mod:`pathlib` used in the test suite.
It tries to import :mod:`pathlib` or :mod:`pathlib2` and falls back to a very
small shim if neither is available.
"""

try:
    from pathlib import Path  # type: ignore
except Exception:  # pragma: no cover - old Python
    try:
        from pathlib2 import Path  # type: ignore
    except Exception:
        import os

        class Path(str):
            """Simplistic Path implementation for Python 3.2."""

            def __new__(cls, *parts):
                return str.__new__(cls, os.path.join(*parts))

            # Basic properties used in tests
            @property
            def suffix(self):
                return os.path.splitext(self)[1]

            @property
            def stem(self):
                return os.path.splitext(os.path.basename(self))[0]

            def open(self, mode="r", *args, **kwargs):
                return open(self, mode, *args, **kwargs)

