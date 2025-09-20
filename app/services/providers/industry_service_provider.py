from app.services.base.industry_service_base import IndustryServiceBase
from app.repositories.providers.industry_repository_provider import IndustryRepositoryProvider
from app.utils.filter.industry_filter import IndustryFilter
from app.configs.db.database import IndustryEntity, UserEntity
from app.schemas.industry_schemas import CreateIndustryDTO, UpdateIndustryDTO
from fastapi import HTTPException, status
from app.utils.res.response_body import ResponseBody
from datetime import datetime

class IndustryServiceProvider(IndustryServiceBase):
    def __init__(self, repository: IndustryRepositoryProvider):
        self.repository = repository

    async def update(self, industry: IndustryEntity, dto: UpdateIndustryDTO) -> IndustryEntity:

        if dto.name is not None and dto.name != industry.name:
            check_name = await self.repository.exists_by_name(dto.name)
            if check_name :
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=dict(ResponseBody[None](
                        code = status.HTTP_409_CONFLICT,
                        message = f"Industry name '{dto.name}' is already in use",
                        body=None,
                        path=None,
                        status=False,
                        timestamp=str(datetime.now()),
                        version=1
                    ))
                )
            
            industry.name = dto.name

        if dto.description is not None:
            industry.description = dto.description

        if dto.icon_url is not None:
            industry.icon_url = dto.icon_url

        if dto.is_active is not None:
            industry.is_active = dto.is_active

        industry.updated_at = datetime.now()
        return await self.repository.save(industry)

    async def get_all_filter(self, filter: IndustryFilter) -> list[IndustryEntity]:
        return await self.repository.get_all_filter(filter)

    async def create(self, user: UserEntity, dto: CreateIndustryDTO) -> IndustryEntity:
        industry = dto.to_entity()
        industry.user_id = user.id

        return await self.repository.add(industry)

    async def get_by_id(self, id: int) -> IndustryEntity | None:
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)

    async def delete(self, industry: IndustryEntity):
        await self.repository.delete(industry)

    async def toggle_is_active(self, industry: IndustryEntity) -> IndustryEntity:
        industry.is_active = not industry.is_active

        return await self.repository.save(industry)