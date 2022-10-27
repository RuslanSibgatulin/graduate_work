# -*- coding: utf-8 -*-

import json

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()


@app.post("/movie")
async def movie_info(request: Request,):
    movie_id = json.loads(await request.body()).get("movie_id")
    return movie_id


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
