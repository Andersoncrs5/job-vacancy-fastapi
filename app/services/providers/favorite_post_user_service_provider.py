from app.services.base.favorite_post_user_service_base import FavoritePostUserServiceBase
from app.configs.db.database import FavoritePostUserEntity, PostUserEntity, UserEntity
from app.repositories.providers.favorite_posts_user_repository_provider import FavoritePostUserRepositoryProvider

class FavoritePostUserServiceProvider(FavoritePostUserServiceBase):
    def __init__(self, repository: FavoritePostUserRepositoryProvider):
        self.repository = repository

    async def delete(self, favo: FavoritePostUserEntity):
        await self.repository.delete(favo)

    
    