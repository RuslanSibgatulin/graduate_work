import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from services.actions import router as actions_router
from services.user import router as profile_router

logger = logging.getLogger("Recom-front")
logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="Recommendations",
    default_response_class=HTMLResponse,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(profile_router)
app.include_router(actions_router)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
