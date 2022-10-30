import uvicorn
from api.v1.recomendations import router as recommendation_router
from db import mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Recommendation API",
    docs_url="/rec/apidocs",
    openapi_url="/rec/apidocs.json",
    default_response_class=ORJSONResponse,
)

app.include_router(recommendation_router, prefix="/rec/v1")


@app.on_event("startup")
async def startup_event():
    mongo.mongo_client = await mongo.get_mongo()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
