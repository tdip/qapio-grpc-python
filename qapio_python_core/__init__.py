from .core.Manifest import load_qapio_manifest
from .QapioContext import QapioContext
from .fsm.FSM import FSM, Action
import json
from time import sleep


def init():
    return QapioContext(load_qapio_manifest())


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

def connect(fn):
    a = fn.start()

    def subscriber(next, *args, **kwargs):

        state = None

        if is_json(next["payload"]):
            state = a.ask(Action(next["type"], json.loads(next["payload"])))
        else:
            state = a.ask(Action(next["type"], next["payload"]))

        execution_response_stream.on_next({"value": json.dumps(state.state_data.__dict__)})

    def oncomplete(next, *args, **kwargs):
        pass

    def onerror(next, *args, **kwargs):
        pass

    try:
        with init() as context:
            io_context = context.io

            execution_response_stream = io_context.open_input('RESPONSE')

            execution_request_stream = io_context.open_output('REQUEST')

            merged_output = execution_request_stream.subscribe(on_next=subscriber, on_error=onerror, on_completed=oncomplete)

            while True:
                sleep(0.1)

    except Exception as ex:
        print("Python has error: " + str(ex))
        traceback = ex.__traceback__

        while traceback:
            print("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
            traceback = traceback.tb_next
        raise ex
