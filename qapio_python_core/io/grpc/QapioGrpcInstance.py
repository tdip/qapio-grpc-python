from google.protobuf.any_pb2 import Any
from grpc import Channel
import itertools as it
import reactivex as rx
from reactivex import operators as op

from typing import List, Union

from ...core import scheduler
from ..serialization.DictionarySerializer import DictionarySerializer

from .proto.GrpcGraphEvaluator_pb2 import OutputRequest
from .proto.GrpcGraphEvaluator_pb2_grpc import GraphEvaluatorStub
from .GrpcInput import GrpcInput

n = 0

def concat_map(os, f):
    def accumulator(state, next):
        # global n
        # n = n + 1
        # print(n)

        (_, previous) = state

        values = list(it.chain(previous, next))
        # print(len(values))
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
        op.subscribe_on(scheduler), op.observe_on(scheduler)
    )


class QapioGrpcInstance(object):

    def __init__(self, channel: Channel):

        self.__channel = channel
        self.__stub = GraphEvaluatorStub(channel)
        self.__serializer = DictionarySerializer

    def open_input(self, graph_id: str, stream_id: str):

        return GrpcInput(self.__stub, graph_id, stream_id, self.__serializer())

    def open_output(self, graph_id: str, stream_id: str):
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
                s = serializer.write_bytes(data.value)
                return s # rx.from_list(serializer.write_bytes(data.value))
            except Exception as e:
                print(data.value)
                print("python dld is screwed... %s" % str(e))
                raise e

        return concat_map(rx.from_iterable(self.__stub.Output(args)), deserialize)
