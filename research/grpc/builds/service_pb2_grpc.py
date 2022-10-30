# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import builds.service_pb2 as service__pb2
import grpc


class MoviesServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMovieInfo = channel.unary_unary(
                '/MoviesService/GetMovieInfo',
                request_serializer=service__pb2.MovieRequest.SerializeToString,
                response_deserializer=service__pb2.Movie.FromString,
                )


class MoviesServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMovieInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MoviesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMovieInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieInfo,
                    request_deserializer=service__pb2.MovieRequest.FromString,
                    response_serializer=service__pb2.Movie.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MoviesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MoviesService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMovieInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MoviesService/GetMovieInfo',
            service__pb2.MovieRequest.SerializeToString,
            service__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)