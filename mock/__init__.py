# Fallback "mock" package for environments where neither unittest.mock
# nor the external "mock" library are available.

from __future__ import absolute_import

try:
    from unittest import mock as _mock  # type: ignore
except Exception:  # pragma: no cover - old Python
    try:
        import mock as _mock  # type: ignore
    except Exception:  # pragma: no cover - old Python
        _mock = None

if _mock is not None:
    globals().update(_mock.__dict__)
else:
    import contextlib
    import importlib

    class _patch(contextlib.ContextDecorator):
        def __init__(self, target, attribute=None, new=None):
            if attribute is None:
                if not isinstance(target, str):
                    raise TypeError("Need a target string when attribute is None")
                target, attribute = target.rsplit('.', 1)
            if isinstance(target, str):
                target = importlib.import_module(target)
            self.target = target
            self.attribute = attribute
            self.new = new
            self.original = None

        def __enter__(self):
            self.original = getattr(self.target, self.attribute)
            setattr(self.target, self.attribute, self.new)
            return self.new

        def __exit__(self, exc_type, exc_value, traceback):
            setattr(self.target, self.attribute, self.original)

    def patch(target, attribute=None, new=None):
        """Simplified replacement for :func:`unittest.mock.patch`."""
        return _patch(target, attribute, new)

__all__ = ['patch']
