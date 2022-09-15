import grpc
from typing import List, Union

from ..core.Manifest import Manifest

from .grpc.QapioGrpcInstance import QapioGrpcInstance


class QapioIOContext(object):

    def __init__(self, manifest: Manifest):
        self.__manifest = manifest

    def __enter__(self, *args, **kwargs):
        #print("opening grpc...")
        self.__channel = grpc.insecure_channel('localhost:5113')
        #print("opened grpc")
        self.__grpc = QapioGrpcInstance(self.__channel)


        return self

    def __exit__(self, *args, **kwargs):
        self.__channel.close()
        self.__grpc = None

    @property
    def request_id(self):
         return self.__manifest.request_id

    def open_input(self, stream_id: str):
        return self.__grpc.open_input(self.__manifest.graph_id, stream_id)

    def open_output(self, stream_id: str):
        return self.__grpc.open_output(self.__manifest.graph_id, stream_id)
