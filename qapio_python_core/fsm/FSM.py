from pykka import ThreadingActor, ActorRef
from typing import Generic, TypeVar, Callable, TypedDict, Any
from copy import deepcopy
from typing import Union

TStateName = TypeVar("TStateName")
TStateData = TypeVar("TStateData")


class Action:
    def __init__(self, action_type: str, payload: Any):
        self.type = action_type
        self.payload = payload


class StateContainer(Generic[TStateName, TStateData]):
    def __init__(self, state_name: TStateName, state_data: TStateData, stop: bool = False):
        self.state_name = state_name
        self.state_data = state_data
        self.stop = stop

    def using(self, state_data: TStateData):
        return StateContainer(self.state_name, state_data)


class FSM(Generic[TStateName, TStateData], ThreadingActor):

    use_daemon_thread = True
    state_data: TStateData = None
    state_name: TStateName = None

    handlers = {}
    _unhandled_handler = None

    def __init__(self):
        self._unhandled_handler = self._unhandled
        super().__init__()

    def _unhandled(self, action_type: str, payload: Any) -> Union[StateContainer[TStateName, TStateData], None]:
        return None

    def start_with(self, state_name: TStateName, state_data: TStateData):
        self.state_data = state_data
        self.state_name = state_name

    def when(self, state_name: TStateName, handler: Callable[[str, Any], Union[StateContainer[TStateName, TStateData], None]]):
        self.handlers[state_name] = handler

    def when_unhandled(self, handler: Callable[[str, Any], Union[StateContainer[TStateName, TStateData], None]]):
        self._unhandled_handler = handler

    def stay(self):
        return StateContainer[TStateName, TStateData](None, None)

    def goto(self, state_name: TStateName):
        return StateContainer[TStateName, TStateData](state_name, None)

    def stop(self):
        return StateContainer[TStateName, TStateData](None, None, True)

    def on_receive(self, message: Action) -> Any:
        if self.state_name is None:
            raise Exception("Initial state name must be set.")

        if self.state_data is None:
            raise Exception("Initial state data must be set.")

        if self.state_name in self.handlers:

            state_name_copy = deepcopy(self.state_name)
            state_data_copy = deepcopy(self.state_data)

            next = self.handlers[self.state_name](message.type, message.payload)

            if next is None:
                next = self._unhandled_handler(message.type, message.payload)

            if next is None:
                print("Unhandled.")
                next = StateContainer[TStateName, TStateData](state_name_copy, state_data_copy)

            if next.stop:
                print("GOODBYE")
                ThreadingActor.stop(self)

            if next.state_data is not None:
                self.state_data = next.state_data
            else:
                self.state_data = state_data_copy

            if next.state_name is not None:
                self.state_name = next.state_name
            else:
                self.state_name = state_name_copy

            return StateContainer[TStateName, TStateData](self.state_name, self.state_data)

        print("Unhandled")

    def reduce(self, action: Action):
        return self.actor_ref.ask(action)
