from abc import ABC, abstractmethod
from app.configs.db.database import MySkillEntity
from uuid import UUID
from app.utils.filter.my_skill_filter import MySkillFilter

class MySkillRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        pass

    @abstractmethod
    async def save(self, my: MySkillEntity) -> MySkillEntity:
        pass

    @abstractmethod
    async def delete(self, my: MySkillEntity):
        pass

    @abstractmethod
    async def add(self, my: MySkillEntity) -> MySkillEntity:
        pass

    @abstractmethod
    async def exists_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_skill_id_and_user_id(self, skill_id: UUID, user_id: int) -> MySkillEntity | None:
        pass