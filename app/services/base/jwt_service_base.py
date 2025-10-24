from abc import ABC, abstractmethod
from typing import Any

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from app.configs.db.database import UserEntity, UserRolesEntity
from fastapi.security import HTTPAuthorizationCredentials

class JwtServiceBase(ABC):

    @abstractmethod
    def throw_unauthorized(self, message: str) -> ORJSONResponse:
        pass

    @abstractmethod
    def check_authorization_boolean_style(self, token: str, roles: list[str]) -> bool:
        pass

    @abstractmethod
    def _check_required_role(self, token: str, required_role: str) -> bool:
        pass

    @abstractmethod
    def create_refresh_token_with_roles(self, user: UserEntity, roles: list[UserRolesEntity]) -> str:
        pass

    @abstractmethod
    def create_access_token_with_roles(self, user: UserEntity, roles: list[UserRolesEntity]) -> str:
        pass

    @abstractmethod
    def _create_token_payload(self, user: UserEntity, roles: list[UserRolesEntity], expires_minutes: float) -> dict[str, Any]:
        pass

    @abstractmethod
    def extract_user_id_v2(self, token: str) -> int:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict | None:
        pass

    @abstractmethod
    def extract_user_id(self, token: str) -> int | None:
        pass

    @abstractmethod
    def extract_email(self, token: str) -> str | None:
        pass

    @abstractmethod
    def valid_credentials(self, creden: HTTPAuthorizationCredentials) -> str:
        pass