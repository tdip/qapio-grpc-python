from google.protobuf.any_pb2 import Any
import itertools
from rx.core.typing import Observer
from typing import Iterable, List, Union

from ..serialization.StreamSerializerBase import StreamSerializerBase

from .proto.GrpcGraphEvaluator_pb2 import InputRequest
from .proto.GrpcGraphEvaluator_pb2_grpc import GraphEvaluatorStub

class GrpcInput(Observer):

    def __init__(self, stub: GraphEvaluatorStub, graphId: str, streamId: str, serializer: StreamSerializerBase):

        self.__stub = stub
        self.__graphId = graphId
        self.__streamId = streamId
        self.__serializer = serializer

    def __serialize(self, payload: dict) -> Iterable[bytes]:
        return self.__serializer.write_object(payload)

    def __serialize_to_any(self, payload: dict) -> Iterable[Any]:

        def to_any(data):
            return Any(value = data)

        return map(to_any, self.__serialize(payload))

    def __to_grpc_payload(self, payload: List[dict]) -> InputRequest:

        serialized_payload = itertools.chain(*map(self.__serialize_to_any, payload))

        return InputRequest(
                graphId = self.__graphId,
                streamId = self.__streamId,
                values = list(serialized_payload)
            )

    def on_next(self, payload: Union[dict, List[dict]]):

        if isinstance(payload, dict):
            payload = [payload]

        # todo: emit several events for big messages

        def generate_route():
            encoded_payload = self.__to_grpc_payload(payload)
            yield encoded_payload
        #self.__stub.Input([encoded_payload])
        self.__stub.Input(generate_route())

    def on_completed(self):
        pass

    def on_error(self, exn):
        raise exn