from app.configs.db.database import AreaEntity
from app.utils.filter.area_filter import AreaFilter
from typing import List
from app.schemas.area_schemas import UpdateAreaDTO, CreateAreaDTO
from app.services.base.area_service_base import AreaServiceBase
from app.repositories.providers.area_repository_provider import AreaRepositoryProvider
from datetime import datetime
from app.utils.res.response_body import ResponseBody
from fastapi import HTTPException, status

class AreaServiceProvider(AreaServiceBase):
    def __init__(self, repository: AreaRepositoryProvider):
        self.repository = repository

    async def toggle_is_active(self, area: AreaEntity) -> AreaEntity:
        area.is_active = not area.is_active
        return await self.repository.save(area)

    async def get_all(self, filter: AreaFilter) -> List[AreaEntity]:
        return await self.repository.get_all(filter)

    async def get_by_id(self, id: int) -> AreaEntity | None:
        return await self.repository.get_by_id(id)

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def exists_by_name(self, name: str) -> bool:
        return await self.repository.exists_by_name(name)

    async def update(self, area: AreaEntity, dto: UpdateAreaDTO) -> AreaEntity:
        
        if dto.name != None and area.name != dto.name:
            check = await self.repository.exists_by_name(dto.name)

            if check == True:
                raise HTTPException(
                    status_code=409,
                    detail=dict(ResponseBody[None](
                        code=409,
                        message=f"Name {dto.name} is in use!",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )

            area.name = dto.name

        if dto.description != None:
            area.description = dto.description

        if dto.is_active != None:
            area.is_active = dto.is_active

        return await self.repository.save(area)

    async def create(self, user_id: int, dto: CreateAreaDTO) -> AreaEntity:
        area  = dto.to_entity()
        area.user_id = user_id

        return await self.repository.add(area)

    async def delete(self, area: AreaEntity):
        await self.repository.delete(area)