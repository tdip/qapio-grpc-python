from .core.Manifest import load_qapio_manifest
from .QapioContext import QapioContext
from fsm import FSM

def init():
    return QapioContext(load_qapio_manifest())
