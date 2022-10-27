# -*- coding: utf-8 -*-

from time import time
import uuid

import grpc

from builds.service_pb2 import MovieRequest
from builds.service_pb2_grpc import MoviesServiceStub


def main():
    with grpc.insecure_channel("localhost:3000") as channel:
        client = MoviesServiceStub(channel)

        start = time()

        for _ in range(2000):
            request = MovieRequest(movie_id=str(uuid.uuid4()))
            resp = client.GetMovieInfo(request)

        print(time() - start)


if __name__ == "__main__":
    main()
