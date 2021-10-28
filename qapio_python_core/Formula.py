import rx.operators as op
import signal
from time import sleep
import os
from . import init
from .core import scheduler


class ExecutionContext:
    def __init__(self):
        self.__running = False

    @property
    def running(self) -> bool:
        return self.__running

    @running.setter
    def running(self, value):
        self.__running = value


def do_work(init_instance, ctx: dict):

    results = init_instance.function(ctx)

    return results


def formula(fn):
    def subscriber(next, *args, **kwargs):

        init_instance = fn()
        data = next["payload"]
        ctx = data
        results = do_work(init_instance, ctx)
        initialize_response_stream.on_next(results)

    def error_subscriber(exn, *args, **kwargs):

        traceback = exn.__traceback__
        while traceback:
            print("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
            traceback = traceback.tb_next
        print("Python has error %s" % str(exn))

    def complete_subscriber(*args, **kwargs):
        # print("Python is bye bye...")
        execution_context.running = False

    def logger(id):
        def f(value):
            print("Python is processing %s:%s" % (id, str(value)))
            return value

        return f

    try:
        with init() as context:

            # print("Python opened context")
            sleep(6)
            io_context = context.io
            initialize_response_stream = io_context.open_input('response')
            initialize_request_stream = io_context.open_output(
                'request')
            merged_output = initialize_request_stream.pipe(
                op.subscribe_on(scheduler), op.observe_on(scheduler)
            )

            execution_context = ExecutionContext()
            execution_context.running = True

            merged_output.pipe(op.map(lambda v: {
                "payload": v
            }), op.take_while(lambda t: "value" not in t["payload"])).subscribe(
                on_next=subscriber,
                on_error=error_subscriber,
                on_completed=complete_subscriber)

            while execution_context.running is True:
                sleep(1)

            os.kill(os.getpid(), signal.SIGTERM)


    except Exception as ex:
        print("Python has error: " + str(ex))
        traceback = ex.__traceback__

        while traceback:
            print("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
            traceback = traceback.tb_next
        raise ex
