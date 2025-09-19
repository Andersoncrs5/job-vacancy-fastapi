from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.configs.db.database import get_db
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.services.providers.user_service_provider import UserServiceProvider
from app.repositories.providers.category_repository_provider import CategoryRepositoryProvider
from app.services.providers.category_service_provider import CategoryServiceProvider
from app.services.providers.jwt_service_provider import JwtServiceProvider
from app.services.base.jwt_service_base import JwtServiceBase
from typing import Final

def get_category_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CategoryServiceProvider:
    repository: Final = CategoryRepositoryProvider(db)
    return CategoryServiceProvider(repository)

def get_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> UserServiceProvider:
    repository: Final = UserRepositoryProvider(db)
    return UserServiceProvider(repository)

def get_jwt_service_dependency() -> JwtServiceBase:
    return JwtServiceProvider()