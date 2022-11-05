from http import HTTPStatus

from core.config import recom_url_content, recom_url_ml
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from fastapi.templating import Jinja2Templates
from models.models import Token
from utils.auth import decode_token, get_access_token
from utils.posters import get_posters
from utils.recommender import get_recommender_movies

router = APIRouter(tags=["Profile"])
templates = Jinja2Templates(directory="templates")
bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse(
        "signin.html", {"request": request}
    )


@router.post("/login", response_class=HTMLResponse)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    token = await get_access_token(form_data.username, form_data.password)
    # token = await get_fake_access_token(form_data.username, form_data.password)

    if not token:
        return await get_login(request)

    payload = decode_token(token)
    request.session["auth_token"] = token.dict()
    request.session["username"] = form_data.username
    request.session["user_id"] = payload["sub"]["user_id"]
    headers = {"Authorization": "Bearer " + token.access_token}

    return RedirectResponse(
        "/",
        status_code=HTTPStatus.FOUND,
        headers=headers
    )


@router.get("/model")
async def ml_filter_page(
    request: Request
):
    if not {"user_id", "username"}.issubset(request.session):
        return RedirectResponse("/login")

    movies = await get_recommender_movies(
        recom_url_ml,
        Token(**request.session["auth_token"])
    )

    movies = get_posters([m.dict() for m in movies])

    return templates.TemplateResponse(
        "album.html",
        {
            "request": request,
            "username": request.session["username"],
            "movies": movies[:10]

        },
    )


@router.get("/base")
async def content_filter_page(
    request: Request
):
    if not {"user_id", "username"}.issubset(request.session):
        return RedirectResponse("/login")

    movies = await get_recommender_movies(
        recom_url_content,
        Token(**request.session["auth_token"])
    )
    movies = get_posters([m.dict() for m in movies])

    return templates.TemplateResponse(
        "album.html",
        {
            "request": request,
            "username": request.session["username"],
            "movies": movies[:10]

        },
    )


@router.get("/")
async def index_page(
    request: Request
):
    if not {"user_id", "username"}.issubset(request.session):
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "featurs.html",
        {
            "request": request,
            "username": request.session["username"]
        },
    )
