from app.services.base.jwt_service_base import JwtServiceBase
import os
from dotenv import load_dotenv
from app.configs.db.database import UserEntity
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody

load_dotenv()

SECRET_KEY: Final[str | None] = os.getenv("SECRET_KEY")
ALGORITHM: Final[str | None] = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: Final[str | None] = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES: Final[str | None] = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

class JwtServiceProvider(JwtServiceBase):

    def create_access_token(self, user: UserEntity) -> str:
        if ACCESS_TOKEN_EXPIRE_MINUTES is None or SECRET_KEY == None or ALGORITHM == None:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not defined")
        
        payload: Final = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
        }

        token: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def create_refresh_token(self, user: UserEntity) -> str:
        if REFRESH_TOKEN_EXPIRE_MINUTES is None or SECRET_KEY == None or ALGORITHM == None:
            raise ValueError("REFRESH_TOKEN_EXPIRE_MINUTES is not defined")
        
        payload: Final = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> dict | None:
        if ACCESS_TOKEN_EXPIRE_MINUTES is None or SECRET_KEY is None or ALGORITHM is None:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not defined")

        try :
            payload: Final = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            return payload
        except JWTError:
            return None

    def extract_user_id(self, token: str) -> int | None:
        payload: Final = self.decode_token(token)

        if payload and "sub" in payload:
            return int(payload["sub"])

        return None

    def extract_user_id_v2(self, token: str) -> int:
        id = self.extract_user_id(token)

        if id is None or id <= 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        return id 

    def extract_email(self, token: str) -> str | None:
        payload: Final = self.decode_token(token)

        if payload and "email" in payload:
            return payload["email"]

        return None

    def valid_credentials(self, creden: HTTPAuthorizationCredentials) -> str:
        scheme: Final[str] = creden.scheme
        if scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="Authorization header invalid",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )
        
        token: Final[str] = creden.credentials

        token_valided: Final[dict[str, str] | None] = self.decode_token(token)

        if token_valided is None :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="Authorization header invalid",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        exp_timestamp = token_valided.get("exp")
        if exp_timestamp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="Token invalid",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        now = datetime.now(UTC).timestamp()
        if now > float(exp_timestamp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="Token invalid",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        return token

    