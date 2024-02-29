from .core.Manifest import load_qapio_manifest
from .QapioContext import QapioContext
from .io.IOContextActor import MainActor
from .fsm.FSM import FSM, Action
from .qapi.Qapi import Qapi, TimeSeriesApi
import json
from time import sleep
import sys
import traceback
from pandas import Timestamp
from pykka import ThreadingActor
from .qapi.client.Client import QapioGrpc
import inspect
import os
# import grpc
# import pykka
# from generated import chat_pb2, chat_pb2_grpc
#
# class MainActor(pykka.ThreadingActor):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         self.channel = grpc.insecure_channel('localhost:50051')
#         self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
#
#     def on_start(self):
#         self.subscription_actor_ref = SubscriptionActor.start(self.actor_ref, self.stub, self.name)
#
#     def on_receive(self, message):
#         if message == "start_computation":
#             self.computation_actor_ref = ComputationActor.start(self.actor_ref, self.subscription_actor_ref)
#         elif isinstance(message, chat_pb2.ComputationResult):
#             self.stub.SendResult(chat_pb2.SendResultRequest(name=self.name, result=message.result))
#
#     def on_stop(self):
#         self.subscription_actor_ref.stop()
#
# class SubscriptionActor(pykka.ThreadingActor):
#     def __init__(self, main_actor_ref, stub, name):
#         super().__init__()
#         self.main_actor_ref = main_actor_ref
#         self.stub = stub
#         self.name = name
#         self.subscription_active = False
#
#     def on_start(self):
#         self.stub.Subscribe(chat_pb2.SubscribeRequest(name=self.name), callback=self.on_message)
#
#     def on_message(self, response):
#         if not self.subscription_active:
#             self.subscription_active = True
#             self.main_actor_ref.tell("start_computation")
#
#         self.actor_ref.proxy().create_computation_actor(response)
#
#     def on_stop(self):
#         self.stub.Unsubscribe(chat_pb2.UnsubscribeRequest())
#
#     def create_computation_actor(self, message):
#         computation_actor_ref = self.actor_ref.proxy().create_computation_actor()
#         computation_actor_ref.tell(message)
#
# class ComputationActor(pykka.ThreadingActor):
#     def __init__(self, main_actor_ref, subscription_actor_ref):
#         super().__init__()
#         self.main_actor_ref = main_actor_ref
#         self.subscription_actor_ref = subscription_actor_ref
#         self.computation_subscription_active = False
#         self.result_subscription_active = False
#
#     def on_receive(self, message):
#         if isinstance(message, chat_pb2.Message) and not self.computation_subscription_active:
#             self.computation_subscription_active = True
#             self.subscription_actor_ref.tell({"message": message, "actor_ref": self.actor_ref.proxy()})
#
#         elif isinstance(message, chat_pb2.ComputationResult) and not self.result_subscription_active:
#             self.result_subscription_active = True
#             self.main_actor_ref.tell(message)
#
#     def on_stop(self):
#         if self.computation_subscription_active:
#             self.subscription_actor_ref.tell({"unsubscribe": True})
#         if self.result_subscription_active:
#             self.main_actor_ref.tell({"unsubscribe": True})
#
# if __name__ == '__main__':
#     system = pykka.ThreadingActorSystem()
#     main_actor_ref = system.actor_of(MainActor, args=('my_name',))
#     main_actor_ref.tell("start")
#
#     input("Press Enter to stop...")
#
#     main_actor_ref.tell("stop")
#     system.stop()
# Ariel Fischer
# import grpc
# import rx
# from rx import operators as ops
# from generated import chat_pb2, chat_pb2_grpc
#
# class GRPCRx:
#     def __init__(self, server_address):
#         self.server_address = server_address
#
#     def subscribe(self, name):
#         channel = grpc.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         response_observable = rx.create(lambda observer, scheduler: self._subscribe(observer, stub, name))
#
#         return response_observable.pipe(
#             ops.map(lambda response: response.message)
#         )
#
#     def _subscribe(self, observer, stub, name):
#         request = chat_pb2.SubscribeRequest(name=name)
#
#         response_iterator = stub.Subscribe(request)
#
#         for response in response_iterator:
#             observer.on_next(response)
#
#         observer.on_completed()
#
#     def unsubscribe(self, name):
#         channel = grpc.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         request = chat_pb2.UnsubscribeRequest(name=name)
#
#         stub.Unsubscribe(request)
#
#     def send_result(self, name, result):
#         channel = grpc.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         request = chat_pb2.SendResultRequest(name=name, result=result)
#
#         response = stub.SendResult(request)
#
#         return response
#
#
#
# import grpc
# import aioreactive as rx
# from aioreactive import operators as ops
# from generated import chat_pb2, chat_pb2_grpc
#
# class GRPCAsync:
#     def __init__(self, server_address):
#         self.server_address = server_address
#
#     async def subscribe(self, name):
#         channel = grpc.aio.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         request = chat_pb2.SubscribeRequest(name=name)
#
#         response_iterator = stub.Subscribe(request)
#
#         return rx.from_iterable(response_iterator).pipe(
#             ops.map(lambda response: response.message)
#         )
#
#     async def unsubscribe(self, name):
#         channel = grpc.aio.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         request = chat_pb2.UnsubscribeRequest(name=name)
#
#         await stub.Unsubscribe(request)
#
#     async def send_result(self, name, result):
#         channel = grpc.aio.insecure_channel(self.server_address)
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#
#         request = chat_pb2.SendResultRequest(name=name, result=result)
#
#         response = await stub.SendResult(request)
#
#         return response

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

class Query(ThreadingActor):
    def __init__(self, api, instance):
        super().__init__()
        self.__api = api
        self.__log = api.api
        self.__instance = instance
        self.__input = api.input("RESPONSE").get()
        self.__logs = api.input("LOG").get()
        api.output("REQUEST", self.actor_ref)

    def on_receive(self, request):
        # message = request["universe"]
        # universeId = request["measurement"]
        # factor = request["factor"]

        params = inspect.signature(self.__instance).parameters

        ordered_args = {param: request.get(param) for param in list(params.keys())}
        self.__logs.proxy().on_next({'value': 'BILLEBA'})

        try:
            self.__input.proxy().on_next({'data': self.__instance(**ordered_args)})
        except Exception as ex:
            self.__logs.proxy().on_next({'value': traceback.format_exc()})
            traceback.print_exc()


def query(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc(os.getenv('GRPC_ENDPOINT') + ':5113', 'http://' + os.getenv('GQL_ENDPOINT') + ':4000/graphql', manifest)
    Query.start(qapio, fn)

def source(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc(os.getenv('GRPC_ENDPOINT') + ':5113', 'http://' + os.getenv('GQL_ENDPOINT') + ':4000/graphql', manifest)
    Query.start(qapio, fn)

def flow(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc(os.getenv('GRPC_ENDPOINT') + ':5113', 'http://' + os.getenv('GQL_ENDPOINT') + ':4000/graphql', manifest)
    Query.start(qapio, fn)

def sink(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc(os.getenv('GRPC_ENDPOINT') + ':5113', 'http://' + os.getenv('GQL_ENDPOINT') + ':4000/graphql', manifest)
    Query.start(qapio, fn)
