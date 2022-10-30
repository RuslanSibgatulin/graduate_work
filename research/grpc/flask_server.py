# -*- coding: utf-8 -*-

import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/movie", methods=["POST"])
def movie_info():
    movie_id = json.loads(request.data).get("movie_id")
    return movie_id


if __name__ == "__main__":
    app.run(port=3001)
