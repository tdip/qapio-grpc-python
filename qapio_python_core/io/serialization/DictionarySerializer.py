from enum import Enum
import json
from typing import Any, Iterable, List

from .StreamDeserializerBase import StreamDeserializerBase
from .StreamSerializerBase import StreamSerializerBase


class State(Enum):
    READ_LENGTH = 1
    READ_OBJECT = 2


class DictionarySerializer(StreamDeserializerBase, StreamSerializerBase):

    def __init__(self):
        self.__data = bytes()
        self.__state = State.READ_LENGTH
        self.__remaining = 0

    def __try_read_length(self):

        if self.__state == State.READ_OBJECT:
            return True

        if len(self.__data) < 4:
            return False

        length_bytes = self.__data[0:4]
        self.__data = self.__data[4:]
        self.__state = State.READ_OBJECT
        self.__remaining = int.from_bytes(length_bytes, byteorder='little')
        print("python is next object length %i" % self.__remaining)

        return True

    def __try_read_next_object(self):

        if self.__state != State.READ_OBJECT:
            raise Exception("Serializer must read length before reading an object")

        if len(self.__data) < self.__remaining:
            return None

        payload_bytes = self.__data[0: self.__remaining]
        self.__data = self.__data[self.__remaining:]
        self.__remaining = 0
        self.__state = State.READ_LENGTH

        return json.loads(payload_bytes.decode("utf-8"))

    def __try_read_next(self):

        return self.__try_read_length() and self.__try_read_next_object()

    def __read_all_objects(self) -> Iterable[Any]:

        next_object = self.__try_read_next()

        while isinstance(next_object, dict):
            print("python is yielding object %s" % str(next_object))
            yield next_object
            next_object = self.__try_read_next()

    def write_bytes(self, data: bytes) -> List[Any]:

        self.__data = self.__data + data

        result = list(self.__read_all_objects())

        print("Python is yielded objects %s" % str(result))

        return result

    def write_object(self, data):

        # todo: chunk big objects
        payload_bytes = bytes(json.dumps(data), 'utf-8')
        payload_length = len(payload_bytes).to_bytes(4, byteorder='little')

        return [payload_length + payload_bytes]
