from abc import ABC, abstractmethod
from typing import Any

from app.configs.db.database import UserEntity, MyRolesEntity
from fastapi.security import HTTPAuthorizationCredentials

class JwtServiceBase(ABC):
    @abstractmethod
    def create_refresh_token_with_roles(self, user: UserEntity, roles: list[MyRolesEntity]) -> str:
        pass

    @abstractmethod
    def create_access_token_with_roles(self, user: UserEntity, roles: list[MyRolesEntity]) -> str:
        pass

    @abstractmethod
    def _create_token_payload(self, user: UserEntity, roles: list[MyRolesEntity], expires_minutes: float) -> dict[str, Any]:
        pass

    @abstractmethod
    def extract_user_id_v2(self, token: str) -> int:
        pass
    
    @abstractmethod
    def create_access_token(self, user: UserEntity) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, user: UserEntity) -> str:
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