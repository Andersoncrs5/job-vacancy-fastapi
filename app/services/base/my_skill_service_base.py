from abc import ABC, abstractmethod
from app.configs.db.database import MySkillEntity
from app.utils.filter.my_skill_filter import MySkillFilter
from app.schemas.my_skill_schemas import CreateMySkillDTO, UpdateMySkillDTO

class MySkillServiceBase(ABC):

    @abstractmethod
    async def create(self, user_id:int, dto: CreateMySkillDTO) -> MySkillEntity:
        pass

    @abstractmethod
    async def update(self, my: MySkillEntity, dto: UpdateMySkillDTO) -> MySkillEntity:
        pass

    @abstractmethod
    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        pass

    @abstractmethod
    async def delete(self, my: MySkillEntity):
        pass

    @abstractmethod
    async def get_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> MySkillEntity | None:
        pass

    @abstractmethod
    async def exists_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> bool:
        pass