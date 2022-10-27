# -*- coding: utf-8 -*-

import json
from time import time
import uuid

import urllib3

http = urllib3.PoolManager()


def main():
    start = time()

    for _ in range(2000):
        http.request(
            "POST",
            "http://localhost:3001/movie",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "movie_id": str(uuid.uuid4())
            })
        )

    print(time() - start)


if __name__ == "__main__":
    main()
