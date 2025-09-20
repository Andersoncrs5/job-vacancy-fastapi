from app.services.base.enterprise_service_base import EnterpriseServiceBase
from app.configs.db.database import EnterpriseEntity, UserEntity, IndustryEntity
from app.schemas.enterprise_schemas import CreateEnterpriseDTO, UpdateEnterpriseDTO
from app.repositories.providers.enterprise_repository_provider import EnterpriseRepositoryProvider
from datetime import datetime
from fastapi import HTTPException, status
from app.utils.res.response_body import ResponseBody
from app.utils.filter.enterprise_filter import EnterpriseFilter

class EnterpriseServiceProvider(EnterpriseServiceBase):
    def __init__(self, repository: EnterpriseRepositoryProvider):
        self.repository = repository

    async def update(self, enter: EnterpriseEntity, dto: UpdateEnterpriseDTO) -> EnterpriseEntity:
        
        if dto.name != None and dto.name !=  enter.name:
            check: bool = await self.repository.exists_by_name(dto.name)
            if check :
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=dict(ResponseBody[None](
                        code = status.HTTP_409_CONFLICT,
                        message = f"Enterprise name '{dto.name}' is already in use",
                        body=None,
                        path=None,
                        status=False,
                        timestamp=str(datetime.now()),
                        version=1
                    ))
                )

            enter.name = dto.name

        if dto.description != None:
            enter.description = dto.description

        if dto.website_url != None:
            enter.website_url = dto.website_url

        if dto.logo_url != None:
            enter.logo_url = dto.logo_url

        enter.updated_at = datetime.now()
        return await self.repository.save(enter)

    async def get_by_id(self, id: int) -> EnterpriseEntity | None:
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)
    
    async def exists_by_name(self, name: str) -> bool:
        return await self.repository.exists_by_name(name)

    async def delete(self, enter: EnterpriseEntity):
        await self.repository.delete(enter)

    async def create(self, industry: IndustryEntity, user: UserEntity ,dto: CreateEnterpriseDTO) -> EnterpriseEntity:
        enter = dto.to_entity()
        enter.user_id = user.id
        enter.industry_id = industry.id

        return await self.repository.add(enter)

    async def get_all_filter(self, filter: EnterpriseFilter) -> list[EnterpriseEntity]:
        return await self.repository.get_all_filter(filter)