from fastapi.security.http import HTTPAuthorizationCredentials as BaseCredentials


class HTTPAuthorizationCredentials(BaseCredentials):
    agent: str

    @classmethod
    def from_base(cls, credentials: BaseCredentials, agent: str):
        return cls(agent=agent, scheme=credentials.scheme, credentials=credentials.credentials)
