from app.configs.db.database import MySkillEntity
from app.utils.filter.my_skill_filter import MySkillFilter
from typing import Final
from app.schemas.my_skill_schemas import CreateMySkillDTO, UpdateMySkillDTO
from app.services.base.my_skill_service_base import MySkillServiceBase
from app.repositories.providers.my_skill_repository_provider import MySkillRepositoryProvider

class MySkillServiceProvider(MySkillServiceBase):
    def __init__(self, repository: MySkillRepositoryProvider):
        self.repository = repository

    async def update(self, my: MySkillEntity, dto: UpdateMySkillDTO) -> MySkillEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(my, field, value)

        return await self.repository.save(my)

    async def create(self, user_id:int, dto: CreateMySkillDTO) -> MySkillEntity:
        my = dto.to_entity()
        my.user_id = user_id

        return await self.repository.add(my)

    async def delete(self, my: MySkillEntity):
        await self.repository.delete(my)

    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        return await self.repository.get_all(filter)

    async def exists_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> bool:
        return await self.repository.exists_by_skill_id_and_user_id(skill_id, user_id)

    async def get_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> MySkillEntity | None:
        return await self.repository.get_by_skill_id_and_user_id(skill_id, user_id)