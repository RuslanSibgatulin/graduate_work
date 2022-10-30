from concurrent import futures

import grpc
from core.config import config
from service.grpc.fake_server.api import MoviesRecommenderService
from service.grpc.proto import recommender_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    recommender_pb2_grpc.add_MoviesRecommenderServicer_to_server(
        MoviesRecommenderService(), server
    )

    server.add_insecure_port(config.GRPC_ADDR)
    server.start()
    print("GRPC server started.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
