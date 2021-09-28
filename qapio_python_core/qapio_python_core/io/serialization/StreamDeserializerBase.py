from typing import Any, List
from abc import ABC, abstractmethod


class StreamDeserializerBase(ABC):

    @abstractmethod
    def write_bytes(self, bss: bytes) -> List[Any]:
        """
        Write the next sequence of bytes from
        the string. If the bytes result in one
        or more new objects deserialized, return
        the object. If not enough bytes have been
        read to produce a new object, simply return
        an empty list.
        """
        pass
