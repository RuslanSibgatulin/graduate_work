import multiprocessing
import socket
from concurrent import futures
from contextlib import contextmanager

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from api import MoviesRecommenderService
from containers import Container
from core.config import settings
from proto import recommender_pb2_grpc


container = Container()
container.config.from_pydantic(settings)
container.wire(modules=["api"])


@contextmanager
def acquire_port(port: int):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    if not sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT):
        raise RuntimeError("Faieled to set SO_REUSERORT")
    
    sock.bind(("", port))
    
    try:
        yield sock.getsockname()
    finally:
        sock.close()

def serve(port: int):
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1),
        interceptors=interceptors,
    )
    recommender_pb2_grpc.add_MoviesRecommenderServicer_to_server(
        MoviesRecommenderService(), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


def main():
    process_count = multiprocessing.cpu_count()

    with acquire_port(settings.app.port) as address:
        workers = []

        for _ in range(process_count):
            worker = multiprocessing.Process(target=serve, args=(settings.app.port,))
            worker.start()
            workers.append(worker)

        for worker in workers:
            worker.join()


if __name__ == "__main__":
    main()
