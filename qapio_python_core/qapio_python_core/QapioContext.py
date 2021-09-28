from .core import Manifest
from .io.QapioIOContext import QapioIOContext


class QapioContext(object):

    def __init__(self, manifest: Manifest):
        self.__manifest = manifest
        self.__io_context = QapioIOContext(manifest)

    def __enter__(self, *args, **kwargs):
        print("opening qapio context")
        self.__io_context.__enter__(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        self.__io_context.__exit__(*args, **kwargs)

    @property
    def io(self) -> QapioIOContext:
        return self.__io_context
