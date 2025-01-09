from pykka import ThreadingActor, ActorRegistry, ActorRef
from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from time import sleep
@dataclass
class Create:
    Guid: Any = None
    Module: str = None
    Type: str = None
    IsClass: bool = None
    Session: str = None
    Props: Any = None

@dataclass
class SessionComplete:
    Session = None

@dataclass
class ReloadModule:
    Module = None

@dataclass
class ApplyAction:
    Module = None
    Type = None
    Session = None
    Props = None

@dataclass
class Request:
    Module: str = None
    Type: str = None
    Session: str = None
    Props: str = None

class Stage(ThreadingActor):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def on_receive(self, message):
        if isinstance(message, Create):
            print(asdict(message))

        if isinstance(message, SessionComplete):
            print("COMPLETE")

class Session(ThreadingActor):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        print("SSSSS")

    def on_receive(self, message):
        if isinstance(message, Create):
            print("MMA")



class QapiCenter(ThreadingActor):

    Children: Dict[str, ActorRef] = {}

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def on_receive(self, message):
        if isinstance(message, Create):
            session = self.Children.get(message.Session)

            if session is not None:
                session.tell(message)
            else:
                session = Session.start()
                self.Children[message.Session] = session
                session.tell(message)

        if isinstance(message, SessionComplete):
            print("djdjd")


        if isinstance(message, ReloadModule):
            print("ØDDs")

        if isinstance(message, ApplyAction):
            print("ØDDd")

        if isinstance(message, Request):
            print("REQUEST")

a = Create(**{'Guid': 454, 'Module': '', 'Type': '', 'Session': '45654', 'IsClass': 4, 'Props': {}})

b = SessionComplete()
c = ReloadModule()
d = ApplyAction()

qapi_center = QapiCenter.start()

qapi_center.tell(a)
qapi_center.tell(b)
qapi_center.tell(c)
qapi_center.tell(d)
qapi_center.tell(a)


ActorRegistry.broadcast(b)
