from app.services.base.industry_service_base import IndustryServiceBase
from app.repositories.providers.industry_repository_provider import IndustryRepositoryProvider
from app.services.generics.generic_service import GenericService
from app.utils.filter.industry_filter import IndustryFilter
from app.configs.db.database import IndustryEntity, UserEntity
from app.schemas.industry_schemas import CreateIndustryDTO, UpdateIndustryDTO
from fastapi import HTTPException, status
from app.utils.res.response_body import ResponseBody
from datetime import datetime
from typing import Final

class IndustryServiceProvider(
    IndustryServiceBase,
    GenericService[
        IndustryEntity,
        IndustryRepositoryProvider,
        IndustryFilter,
    ]
):
    def __init__(self, repository: IndustryRepositoryProvider):
        super().__init__(repository)

    async def exists_by_name(self, name: str) -> bool:
        return await self.repository.exists_by_name(name)

    async def update(self, industry: IndustryEntity, dto: UpdateIndustryDTO) -> IndustryEntity:
        if dto.name is not None and dto.name != industry.name:
            check_name = await self.repository.exists_by_name(dto.name)
            if check_name :
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=dict(ResponseBody(
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

    async def create(self, user: UserEntity, dto: CreateIndustryDTO) -> IndustryEntity:
        industry: Final[IndustryEntity] = dto.to_entity()
        industry.user_id = user.id

        return await self.repository.add(industry)

    async def toggle_is_active(self, industry: IndustryEntity) -> IndustryEntity:
        industry.is_active = not industry.is_active

        return await self.repository.save(industry)