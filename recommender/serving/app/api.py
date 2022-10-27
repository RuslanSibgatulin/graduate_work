import grpc
from dependency_injector.wiring import Provide, inject

from containers import Container
from proto import recommender_pb2, recommender_pb2_grpc
from services import RecommenderService


class MoviesRecommenderService(recommender_pb2_grpc.MoviesRecommenderServicer):
    @inject
    def __init__(
        self,
        recommender: RecommenderService = Provide[Container.recommender],
    ):
        self.recommender = recommender

    def GetRecommendations(
        self,
        request: recommender_pb2.GetRecommendationsRequest,
        _: grpc.ServicerContext,
    ) -> recommender_pb2.GetRecommendationsResponse:
        movies = self.recommender.recommend(request.user_id, request.views)
        return recommender_pb2.GetRecommendationsResponse(
            movies=[
                recommender_pb2.MovieContext(movie_id=movie_id) for movie_id in movies
            ]
        )
