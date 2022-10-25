# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from random import randrange

import grpc

from builds.service_pb2 import Movie, MovieRequest
from builds.service_pb2_grpc import (
    MoviesServiceServicer, add_MoviesServiceServicer_to_server)


class Service(MoviesServiceServicer):

    def GetMovieInfo(
        self, request: MovieRequest, context: grpc.ServicerContext
    ):
        return Movie(
            movie_id=request.movie_id,
            title="Film title",
            score=randrange(3, 10)
        )


def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_MoviesServiceServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:3000")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()
