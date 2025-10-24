from fastapi.responses import ORJSONResponse

from app.configs.commands.command_linner import ROLE_ADM, ROLE_MASTER, ROLE_SUPER_ADM, ROLE_USER, ROLE_ENTERPRISE
from app.services.base.jwt_service_base import JwtServiceBase
import os
from dotenv import load_dotenv
from app.configs.db.database import UserEntity, UserRolesEntity
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing import Final, Any
from app.utils.res.response_body import ResponseBody

load_dotenv()

SECRET_KEY: Final[str | None] = os.getenv("SECRET_KEY")
ALGORITHM: Final[str | None] = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: Final[str | None] = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES: Final[str | None] = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

class JwtServiceProvider(JwtServiceBase):

    def throw_unauthorized(self, message: str) -> ORJSONResponse:
        response_body = ResponseBody(
            code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            body=None,
            status=False,
            timestamp=str(datetime.now()),
            path=None,
            version=1
        )

        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response_body.model_dump()
        )

    def _check_required_role(self, token: str, required_role: str):
        if required_role is None or required_role == "":
            return False

        try:
            payload = self.decode_token(token)
        except Exception as e:
            return False

        roles = payload.get('roles', [])

        if required_role not in roles:
            return False

        return True

    def check_authorization_boolean_style(self, token: str, roles: list[str]) -> bool:
        is_authorized = False

        if len(roles) == 0:
            return is_authorized

        for role in roles:
            if self._check_required_role(token, role):
                is_authorized = True
                break

        return is_authorized

    def _create_token_payload(self, user: UserEntity, roles: list[UserRolesEntity], expires_minutes: float) -> dict[str, Any]:
        names_role = [role_association.role.title for role_association in roles]

        now = datetime.now(UTC)
        expiration = now + timedelta(minutes=expires_minutes)

        payload: Final = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "roles": names_role,
            "iat": now,
            "exp": expiration
        }
        return payload

    def create_access_token_with_roles(self, user: UserEntity, roles: list[UserRolesEntity]) -> str:
        if ACCESS_TOKEN_EXPIRE_MINUTES is None or SECRET_KEY is None or ALGORITHM is None:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not defined or key is missing.")

        payload = self._create_token_payload(user, roles, float(ACCESS_TOKEN_EXPIRE_MINUTES))

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token_with_roles(self, user: UserEntity, roles: list[UserRolesEntity]) -> str:
        if REFRESH_TOKEN_EXPIRE_MINUTES is None or SECRET_KEY is None or ALGORITHM is None:
            raise ValueError("REFRESH_TOKEN_EXPIRE_MINUTES is not defined or key is missing.")

        payload = self._create_token_payload(user, roles, float(REFRESH_TOKEN_EXPIRE_MINUTES))

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