from typing import Any
from fastapi.responses import JSONResponse

try:
    import msgspec # type: ignore
except ImportError: # pragma: nocover
    msgspec = None # type: ignore

class msgspec_jsonresponse(JSONResponse):
    """
    JSON Response using the high-performance msgspec lib to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        assert msgspec is not None, "msgspec must be installed to use msgspec_jsonresponse"
        return msgspec.json.encode(content)
