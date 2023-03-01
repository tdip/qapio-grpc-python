from pykka import ThreadingActor
from reactivex import interval
import sys
from typing import List, Union, TypedDict
from qapio_python_core import load_qapio_manifest
from qapio_python_core.core import Manifest
from google.protobuf.any_pb2 import Any
from grpc import Channel
import itertools as it
import reactivex as rx
from reactivex import operators as op
from qapio_python_core.io.serialization.DictionarySerializer import DictionarySerializer
import grpc
from qapio_python_core.io.grpc.proto.GrpcGraphEvaluator_pb2 import OutputRequest
from qapio_python_core.io.grpc.proto.GrpcGraphEvaluator_pb2_grpc import GraphEvaluatorStub
from pandas import Timestamp, DataFrame, Series, Timedelta, offsets, MultiIndex, to_datetime
from qapio_python_core.io.grpc.GrpcInput import GrpcInput
from qapio_python_core.qapi.Qapi import Qapi
def print_to_stderr(*a):

    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file=sys.stderr)
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
        op.map(lambda x: x[0])
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





class APIActor(ThreadingActor):
    def __init__(self, grpc_endpoint: str, manifest: Manifest):
        super().__init__()
        self.__manifest = manifest
        self.__channel = grpc.insecure_channel(grpc_endpoint)
        self.__grpc = QapioGrpcInstance(self.__channel)
    def open_input(self, stream_id):
        return InputActor.start(self.__manifest, self.__grpc, stream_id, self.actor_ref)

    def open_output(self, stream_id, receiver):
        OutputActor.start(self.__manifest, self.__grpc, stream_id, receiver, self.actor_ref)

    def on_receive(self, message: Any) -> Any:
        print_to_stderr(message)


class QapioGrpc:
    def __init__(self, grpc_endpoint: str, gql_endpoint: str, manifest: Manifest):
        self.api = APIActor.start(grpc_endpoint, manifest)
        self.__qapi = Qapi(gql_endpoint, sync=True)
    def input(self, stream_id):
        print("LD")
        return self.api.proxy().open_input(stream_id)

    def output(self, stream_id, receiver):
        print("LDG")
        self.api.proxy().open_output(stream_id, receiver)

    @property
    def qapi(self):
        return self.__qapi

class InputActor(ThreadingActor):
    def __init__(self, manifest, grpc_instance, stream_id, api):
        super().__init__()
        self.__input = grpc_instance.open_input(manifest.graph_id, stream_id)
    def on_next(self, value):
        self.__input.on_next(value)


class OutputActor(ThreadingActor):
    def __init__(self, manifest, grpc_instance, stream_id, f, api):
        super().__init__()
        grpc_instance.open_output(manifest.graph_id, stream_id).subscribe(lambda x: f.tell(x))
