# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import GrpcGraphEvaluator_pb2 as GrpcGraphEvaluator__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


class GraphEvaluatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Evaluate = channel.unary_stream(
                '/GrpcGraphEvaluator.GraphEvaluator/Evaluate',
                request_serializer=GrpcGraphEvaluator__pb2.GraphDefinition.SerializeToString,
                response_deserializer=GrpcGraphEvaluator__pb2.GraphEvaluatorMessage.FromString,
                )
        self.Input = channel.stream_unary(
                '/GrpcGraphEvaluator.GraphEvaluator/Input',
                request_serializer=GrpcGraphEvaluator__pb2.InputRequest.SerializeToString,
                response_deserializer=GrpcGraphEvaluator__pb2.InputResult.FromString,
                )
        self.Output = channel.unary_stream(
                '/GrpcGraphEvaluator.GraphEvaluator/Output',
                request_serializer=GrpcGraphEvaluator__pb2.OutputRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_any__pb2.Any.FromString,
                )


class GraphEvaluatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Evaluate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Input(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Output(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GraphEvaluatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Evaluate': grpc.unary_stream_rpc_method_handler(
                    servicer.Evaluate,
                    request_deserializer=GrpcGraphEvaluator__pb2.GraphDefinition.FromString,
                    response_serializer=GrpcGraphEvaluator__pb2.GraphEvaluatorMessage.SerializeToString,
            ),
            'Input': grpc.stream_unary_rpc_method_handler(
                    servicer.Input,
                    request_deserializer=GrpcGraphEvaluator__pb2.InputRequest.FromString,
                    response_serializer=GrpcGraphEvaluator__pb2.InputResult.SerializeToString,
            ),
            'Output': grpc.unary_stream_rpc_method_handler(
                    servicer.Output,
                    request_deserializer=GrpcGraphEvaluator__pb2.OutputRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_any__pb2.Any.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'GrpcGraphEvaluator.GraphEvaluator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GraphEvaluator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Evaluate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/GrpcGraphEvaluator.GraphEvaluator/Evaluate',
            GrpcGraphEvaluator__pb2.GraphDefinition.SerializeToString,
            GrpcGraphEvaluator__pb2.GraphEvaluatorMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Input(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/GrpcGraphEvaluator.GraphEvaluator/Input',
            GrpcGraphEvaluator__pb2.InputRequest.SerializeToString,
            GrpcGraphEvaluator__pb2.InputResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Output(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/GrpcGraphEvaluator.GraphEvaluator/Output',
            GrpcGraphEvaluator__pb2.OutputRequest.SerializeToString,
            google_dot_protobuf_dot_any__pb2.Any.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
