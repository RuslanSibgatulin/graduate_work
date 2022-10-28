from random import choice

import grpc

from service.grpc.proto import recommender_pb2, recommender_pb2_grpc


MOVIES = [
    "b1f1e8a6-e310-47d9-a93c-6a7b192bac0e",
    "50fb4de9-e4b3-4aca-9f2f-00a48f12f9b3",
    "fda827f8-d261-4c23-9e9c-e42787580c4d",
    "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
    "025c58cd-1b7e-43be-9ffb-8571a613579b",
    "57beb3fd-b1c9-4f8a-9c06-2da13f95251c",
    "c9e1f6f0-4f1e-4a76-92ee-76c1942faa97",
    "b1384a92-f7fe-476b-b90b-6cec2b7a0dce",
    "118fd71b-93cd-4de5-95a4-e1485edad30e",
    "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f",
    "6e5cd268-8ce4-45f9-87d2-52f0f26edc9e",
    "4b6977e2-b3db-4f04-b83e-f091c6fcd49c",
    "50d842be-bcda-401e-90de-b06929611ce0",
    "9d284e83-21f0-4073-aac0-4abee51193d8",
    "bfe61bd9-5dfd-41ca-80ae-8eca998bc29d",
    "8cc3c3aa-e531-4eeb-a707-08119024b3ea",
    "78efe505-6ef8-41f7-88ef-15840be2e680",
    "192b3fc9-97e2-4260-91c6-a9b91a41e520",
    "c97c8fbc-4084-4e9b-a486-eb5fcfe6104b",
    "15c8d623-7b06-48a9-8cdb-feedfbf6e994"
]


class MoviesRecommenderService(recommender_pb2_grpc.MoviesRecommenderServicer):
    def GetRecommendations(
        self,
        request: recommender_pb2.GetRecommendationsRequest,
        _: grpc.ServicerContext,
    ) -> recommender_pb2.GetRecommendationsResponse:
        movies = set()
        for num in range(7):
            movie = choice(MOVIES)
            movies.add(movie)
        return recommender_pb2.GetRecommendationsResponse(
            movies=[
                recommender_pb2.MovieContext(movie_id=movie_id) for movie_id in list(movies)
            ]
        )