from enum import Enum
from typing import Any, TypeVar, Type

from ...JsonEncoder import Decoder


class BytesDecoder(Decoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return isinstance(element, str)

    @staticmethod
    def decode(element: str, _) -> bytes:
        return element.encode()
