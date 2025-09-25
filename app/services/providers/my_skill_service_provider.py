from app.configs.db.database import MySkillEntity
from uuid import UUID
from app.utils.filter.my_skill_filter import MySkillFilter
from datetime import datetime
from typing import Final
from app.schemas.my_skill_schemas import CreateMySkillDTO
from app.services.base.my_skill_service_base import MySkillServiceBase
from app.repositories.providers.my_skill_repository_provider import MySkillRepositoryProvider

class MySkillServiceProvider(MySkillServiceBase):
    def __init__(self, repository: MySkillRepositoryProvider):
        self.repository = repository

    async def update(self, my: MySkillEntity, dto: CreateMySkillDTO) -> MySkillEntity:
        if dto.proficiency != None:
            my.proficiency = dto.proficiency

        if dto.certificate_url != None:
            my.certificate_url = dto.certificate_url

        if dto.datails != None:
            my.datails = dto.datails

        if dto.years_of_experience != None:
            my.years_of_experience = dto.years_of_experience

        if dto.last_used_date != None:
            my.last_used_date = dto.last_used_date

        return await self.repository.save(my)

    async def create(self, user_id:int, dto: CreateMySkillDTO) -> MySkillEntity:
        my = dto.to_entity()
        my.user_id = user_id

        return await self.repository.add(my)

    async def delete(self, my: MySkillEntity):
        await self.repository.delete(my)

    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        return await self.repository.get_all(filter)

    async def exists_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> bool:
        return await self.repository.exists_by_skill_id_and_user_id(skill_id, user_id)

    async def get_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> MySkillEntity | None:
        return await self.repository.get_by_skill_id_and_user_id(skill_id, user_id)