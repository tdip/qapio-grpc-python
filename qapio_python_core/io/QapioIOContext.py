import grpc
from rx.core.typing import Observer, Observable
from typing import List, Union

from ..core.Manifest import Manifest

from .grpc.QapioGrpcInstance import QapioGrpcInstance


class QapioIOContext(object):

    def __init__(self, manifest: Manifest):
        self.__manifest = manifest

    def __enter__(self, *args, **kwargs):
        print("opening grpc...")
        self.__channel = grpc.insecure_channel('localhost:5000')
        print("opened grpc")
        self.__grpc = QapioGrpcInstance(self.__channel)
        return self

    def __exit__(self, *args, **kwargs):
        self.__grpc = None

    def open_input(self, stream_id: str) -> Observer[Union[dict, List[dict]]]:
        return self.__grpc.open_input(self.__manifest.graph_id, stream_id)

    def open_output(self, stream_id: str) -> Observable[dict]:
        return self.__grpc.open_output(self.__manifest.graph_id, stream_id)
