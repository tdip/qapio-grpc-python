#import grpc
#import pykka
#from generated import chat_pb2, chat_pb2_grpc
#
# class ChatActor(pykka.ThreadingActor):
#     def __init__(self, receiver):
#         super().__init__()
#         self.receiver = receiver
#         self.channel = grpc.insecure_channel('localhost:50051')
#         self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
#
#     def on_receive(self, message):
#         if isinstance(message, str):
#             self.stub.Subscribe(chat_pb2.SubscribeRequest(name=message), callback=self.on_message)
#
#     def on_message(self, response):
#         self.receiver.tell(response.message)
#
# class ReceiverActor(pykka.ThreadingActor):
#     def on_receive(self, message):
#         print(f"Received message: {message}")
#
# if __name__ == '__main__':
#     system = pykka.ThreadingActorSystem()
#     receiver_actor_ref = system.actor_of(ReceiverActor)
#     chat_actor_ref = system.actor_of(ChatActor, args=(receiver_actor_ref,))
#
#     chat_actor_ref.tell("my_name")
#import grpc
#import pykka
#from generated import chat_pb2, chat_pb2_grpc
#
# class ChatActor(pykka.ThreadingActor):
#     def __init__(self, receiver):
#         super().__init__()
#         self.receiver = receiver
#         self.channel = grpc.insecure_channel('localhost:50051')
#         self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
#
#     def on_receive(self, message):
#         if isinstance(message, str):
#             self.stub.Subscribe(chat_pb2.SubscribeRequest(name=message), callback=self.on_message)
#
#     def on_message(self, response):
#         self.receiver.tell(response.message)
#
# class ReceiverActor(pykka.ThreadingActor):
#     def on_receive(self, message):
#         print(f"Received message: {message}")
#
# if __name__ == '__main__':
#     system = pykka.ThreadingActorSystem()
#     receiver_actor_ref = system.actor_of(ReceiverActor)
#     chat_actor_ref = system.actor_of(ChatActor, args=(receiver_actor_ref,))
#
#     chat_actor_ref.tell("my_name")
