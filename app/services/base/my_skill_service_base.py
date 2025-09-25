from abc import ABC, abstractmethod
from app.configs.db.database import MySkillEntity
from uuid import UUID
from app.utils.filter.my_skill_filter import MySkillFilter
from datetime import datetime
from typing import Final
from app.schemas.my_skill_schemas import CreateMySkillDTO

class MySkillServiceBase(ABC):

    @abstractmethod
    async def create(self, user_id:int, dto: CreateMySkillDTO) -> MySkillEntity:
        pass

    @abstractmethod
    async def update(self, my: MySkillEntity, dto: CreateMySkillDTO) -> MySkillEntity:
        pass

    @abstractmethod
    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        pass

    @abstractmethod
    async def delete(self, my: MySkillEntity):
        pass

    @abstractmethod
    async def get_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> MySkillEntity | None:
        pass

    @abstractmethod
    async def exists_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> bool:
        pass