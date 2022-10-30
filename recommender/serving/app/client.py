import logging

import grpc

import proto.recommender_pb2 as recommender_pb2
import proto.recommender_pb2_grpc as recommender_pb2_grpc


def run():
    from time import time

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = recommender_pb2_grpc.MoviesRecommenderStub(channel)
        s = time()
        response = stub.GetRecommendations(
            recommender_pb2.GetRecommendationsRequest(
                user_id="42",
                views=[
                    recommender_pb2.ViewContext(movie_id=movie_id)
                    for movie_id in ["110", "2067", "3147", "1247"]
                ],
            )
        )
        print(response)
        print(time() - s)


if __name__ == "__main__":
    logging.basicConfig()
    run()
