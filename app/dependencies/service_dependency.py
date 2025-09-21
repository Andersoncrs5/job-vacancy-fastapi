from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.configs.db.database import get_db
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.services.providers.user_service_provider import UserServiceProvider
from app.repositories.providers.enterprise_repository_provider import EnterpriseRepositoryProvider
from app.services.providers.enterprise_service_provider import EnterpriseServiceProvider
from app.repositories.providers.favorite_posts_user_repository_provider import FavoritePostUserRepositoryProvider
from app.services.providers.favorite_post_user_service_provider import FavoritePostUserServiceProvider
from app.repositories.providers.industry_repository_provider import IndustryRepositoryProvider
from app.services.providers.industry_service_provider import IndustryServiceProvider
from app.repositories.providers.category_repository_provider import CategoryRepositoryProvider
from app.repositories.providers.post_user_repository_provider import PostUserRepositoryProvider
from app.services.providers.category_service_provider import CategoryServiceProvider
from app.services.providers.post_user_service_provider import PostUserServiceProvider
from app.services.providers.jwt_service_provider import JwtServiceProvider
from app.services.base.jwt_service_base import JwtServiceBase
from typing import Final

def get_favorite_posts_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FavoritePostUserServiceProvider:
    repository: Final = FavoritePostUserRepositoryProvider(db)
    return FavoritePostUserServiceProvider(repository)

def get_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> EnterpriseServiceProvider:
    repository: Final = EnterpriseRepositoryProvider(db)
    return EnterpriseServiceProvider(repository)

def get_industry_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> IndustryServiceProvider:
    repository: Final = IndustryRepositoryProvider(db)
    return IndustryServiceProvider(repository)

def get_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> PostUserServiceProvider:
    repository: Final = PostUserRepositoryProvider(db)
    return PostUserServiceProvider(repository)

def get_category_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CategoryServiceProvider:
    repository: Final = CategoryRepositoryProvider(db)
    return CategoryServiceProvider(repository)

def get_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> UserServiceProvider:
    repository: Final = UserRepositoryProvider(db)
    return UserServiceProvider(repository)

def get_jwt_service_dependency() -> JwtServiceBase:
    return JwtServiceProvider()