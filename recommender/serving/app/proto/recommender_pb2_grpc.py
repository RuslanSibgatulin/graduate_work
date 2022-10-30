# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import proto.recommender_pb2 as recommender__pb2


class MoviesRecommenderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetRecommendations = channel.unary_unary(
            "/MoviesRecommender.MoviesRecommender/GetRecommendations",
            request_serializer=recommender__pb2.GetRecommendationsRequest.SerializeToString,
            response_deserializer=recommender__pb2.GetRecommendationsResponse.FromString,
        )


class MoviesRecommenderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetRecommendations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MoviesRecommenderServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetRecommendations": grpc.unary_unary_rpc_method_handler(
            servicer.GetRecommendations,
            request_deserializer=recommender__pb2.GetRecommendationsRequest.FromString,
            response_serializer=recommender__pb2.GetRecommendationsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "MoviesRecommender.MoviesRecommender", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class MoviesRecommender(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetRecommendations(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/MoviesRecommender.MoviesRecommender/GetRecommendations",
            recommender__pb2.GetRecommendationsRequest.SerializeToString,
            recommender__pb2.GetRecommendationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
