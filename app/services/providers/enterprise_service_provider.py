from app.services.base.enterprise_service_base import EnterpriseServiceBase
from app.configs.db.database import EnterpriseEntity, UserEntity, IndustryEntity
from app.schemas.enterprise_schemas import CreateEnterpriseDTO, UpdateEnterpriseDTO
from app.repositories.providers.enterprise_repository_provider import EnterpriseRepositoryProvider
from datetime import datetime
from fastapi import HTTPException, status

from app.services.generics.generic_service import GenericService
from app.utils.res.response_body import ResponseBody
from app.utils.filter.enterprise_filter import EnterpriseFilter

class EnterpriseServiceProvider(
    EnterpriseServiceBase,
    GenericService[
        EnterpriseEntity,
        EnterpriseRepositoryProvider,
        EnterpriseFilter
    ]
):
    def __init__(self, repository: EnterpriseRepositoryProvider):
        super().__init__(repository)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def update(self, enter: EnterpriseEntity, dto: UpdateEnterpriseDTO) -> EnterpriseEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(enter, field, value)

        enter.updated_at = datetime.now()
        return await self.repository.save(enter)

    async def get_by_user_id(self, user_id: int) -> EnterpriseEntity | None:
        if user_id is None or user_id <= 0:
            return None

        return await self.repository.get_by_user_id(user_id)
    
    async def exists_by_name(self, name: str) -> bool:
        return await self.repository.exists_by_name(name)

    async def create(self, industry: IndustryEntity, user: UserEntity ,dto: CreateEnterpriseDTO) -> EnterpriseEntity:
        enter = dto.to_entity()
        enter.user_id = user.id
        enter.industry_id = industry.id

        return await self.repository.add(enter)