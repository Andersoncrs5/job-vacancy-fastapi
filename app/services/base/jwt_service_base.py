from abc import ABC, abstractmethod
from app.configs.db.database import UserEntity
from fastapi.security import HTTPAuthorizationCredentials

class JwtServiceBase(ABC):
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