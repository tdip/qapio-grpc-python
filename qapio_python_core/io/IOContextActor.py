import pykka
from .grpc.QapioGrpcInstance import QapioGrpcInstance
import grpc
import os

from ..core.Manifest import Manifest
class MainActor(pykka.ThreadingActor):
    def __init__(self, manifest: Manifest):
        super().__init__()
        self.__manifest = manifest
        self.__enter__()

    def __enter__(self, *args, **kwargs):
        self.__channel = grpc.insecure_channel(os.getenv('GRPC_ENDPOINT') + ':5113')
        self.__grpc = QapioGrpcInstance(self.__channel)
        return self

    def __exit__(self, *args, **kwargs):
        self.__channel.close()
        self.__grpc = None
