from app.services.base.skill_service_base import SkillServiceBase
from app.repositories.providers.skill_repository_provider import SkillRepositoryProvider
from uuid import UUID
from typing import Final
from app.utils.filter.skill_filter import SkillFilter
from fastapi import HTTPException
from app.configs.db.database import SkillEntity
from app.schemas.skill_schemas import SkillOUT, CreateSkillDTO, UpdateSkillDTO
from typing import List
from datetime import datetime
from app.utils.res.response_body import ResponseBody

class SkillServiceProvider(SkillServiceBase):
    def __init__(self, repository: SkillRepositoryProvider):
        self.repository = repository

    async def toggle_is_active(self, skill: SkillEntity) -> SkillEntity: 
        skill.is_active = not skill.is_active

        return await self.repository.save(skill)

    async def update(self, skill: SkillEntity, dto: UpdateSkillDTO) -> SkillEntity:

        if dto.name != None and skill.name != dto.name:
            check_name = await self.repository.exists_by_name(dto.name)
            if check_name == True:
                raise HTTPException(
                    status_code=409, 
                    detail=dict(ResponseBody[None](
                        message=f"Name {dto.name} is in use",
                        code=409,
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )

            skill.name = dto.name

        if dto.is_active != None:
            skill.is_active = dto.is_active

        return await self.repository.save(skill)

    async def create(self, dto: CreateSkillDTO) -> SkillEntity:
        skill = dto.to_entity()

        return await self.repository.add(skill)

    async def delete(self, skill: SkillEntity):
        await self.repository.delete(skill)

    async def exists_by_id(self, id: UUID) -> bool:
        return await self.repository.exists_by_id(id)

    async def get_by_id(self, id: UUID) -> SkillEntity | None:
        return await self.repository.get_by_id(id)

    