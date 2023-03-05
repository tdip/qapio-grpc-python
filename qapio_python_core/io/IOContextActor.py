import pykka
from .grpc.QapioGrpcInstance import QapioGrpcInstance
import grpc

from ..core.Manifest import Manifest
class MainActor(pykka.ThreadingActor):
    def __init__(self, manifest: Manifest):
        super().__init__()
        self.__manifest = manifest
        self.__enter__()

    def __enter__(self, *args, **kwargs):
        self.__channel = grpc.insecure_channel('localhost:5113')
        self.__grpc = QapioGrpcInstance(self.__channel)
        return self

    def __exit__(self, *args, **kwargs):
        self.__channel.close()
        self.__grpc = None
