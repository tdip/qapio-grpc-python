from .core.Manifest import load_qapio_manifest
from .QapioContext import QapioContext

def init():
    return QapioContext(load_qapio_manifest())
