from typing import Any, Iterable
from abc import ABC, abstractmethod

class StreamSerializerBase(ABC):

    @abstractmethod
    def write_object(self, next: Any) -> Iterable[bytes]:
        """
        Generate a stream of byte strings that represent
        the data of the provided object. This stream
        must be prefixed by the length encoded as
        4 bytes little endian.
        """
        pass
