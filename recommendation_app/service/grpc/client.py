import grpc.aio

from core.config import config
import service.grpc.proto.recommender_pb2 as recommender_pb2
import service.grpc.proto.recommender_pb2_grpc as recommender_pb2_grpc


class GRPCModelClient:
    @classmethod
    async def get_movies(cls, user_id: str, movies_list: list[str]) -> list[str]:
        async with grpc.aio.insecure_channel(config.GRPC_ADDR) as channel:
            stub = recommender_pb2_grpc.MoviesRecommenderStub(channel)
            response = await stub.GetRecommendations(
                recommender_pb2.GetRecommendationsRequest(
                    user_id=user_id,
                    views=[recommender_pb2.ViewContext(movie_id=movie_id) for movie_id in movies_list],
                )
            )
        return response
