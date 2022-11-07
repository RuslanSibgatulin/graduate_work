from fastapi.security import HTTPBearer as HTTPBearerBase
from models.credentials import HTTPAuthorizationCredentials
from starlette.requests import Request


class HTTPBearer(HTTPBearerBase):
    async def __call__(self, request: Request):
        credentials = await super(HTTPBearer, self).__call__(request)
        agent = request.headers["user-agent"]
        return HTTPAuthorizationCredentials.from_base(credentials, agent)
