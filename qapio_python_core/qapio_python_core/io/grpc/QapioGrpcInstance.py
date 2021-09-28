from google.protobuf.any_pb2 import Any
from grpc import Channel
import itertools as it
import rx
import rx.operators as op
from rx.core.typing import Observer, Observable
from typing import List, Union

from ...core import scheduler
from ..serialization.DictionarySerializer import DictionarySerializer

from .proto.GrpcGraphEvaluator_pb2 import OutputRequest
from .proto.GrpcGraphEvaluator_pb2_grpc import GraphEvaluatorStub
from .GrpcInput import GrpcInput


def concat_map(os: Observable, f):
    def accumulator(state, next):
        (_, previous) = state
        values = list(it.chain(previous, next))

        if len(values) > 0:
            return [values[0]], values[1:]
        else:
            return [], []

    return os.pipe(
        op.map(f),
        op.scan(accumulator, ([], [])),
        op.map(lambda x: x[0]),
        op.filter(lambda x: len(x) > 0),
        op.map(lambda x: x[0]),
        op.subscribe_on(scheduler)
    )


class QapioGrpcInstance(object):

    def __init__(self, channel: Channel):

        self.__channel = channel
        self.__stub = GraphEvaluatorStub(channel)
        self.__serializer = DictionarySerializer

    def open_input(self, graph_id: str, stream_id: str) -> Observer[Union[dict, List[dict]]]:

        return GrpcInput(self.__stub, graph_id, stream_id, self.__serializer())

    def open_output(self, graph_id: str, stream_id: str) -> Observable[dict]:
        """
        Opens a output_stream (from Qapio's perspective) which
        allows qapio to push values into python. This stream
        is abstracted into an Observable so it can be transformed
        with all the power of RX
        """

        args = OutputRequest(graphId=graph_id, streamId=stream_id)

        serializer = self.__serializer()

        def deserialize(data: Any):
            try:
                return serializer.write_bytes(data.value)  # rx.from_list(serializer.write_bytes(data.value))
            except Exception as e:
                print("python is screwed... %s" % str(e))
                raise e

        return concat_map(rx.from_iterable(self.__stub.Output(args)), deserialize)
