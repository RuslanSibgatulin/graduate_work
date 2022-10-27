from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from api import MoviesRecommenderService
from containers import Container
from core.config import settings
from proto import recommender_pb2_grpc


container = Container()
container.config.from_pydantic(settings)
container.wire(modules=["api"])


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1),
        interceptors=interceptors,
    )
    recommender_pb2_grpc.add_MoviesRecommenderServicer_to_server(
        MoviesRecommenderService(), server
    )

    server.add_insecure_port(f"[::]:{settings.app.port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
