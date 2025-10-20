from typing import TypeVar, Generic

T_Entity = TypeVar('T_Entity')
T_Repo = TypeVar('T_Repo')
T_Filter = TypeVar('T_Filter')

class GenericService(Generic[T_Entity, T_Repo, T_Filter]):
    def __init__(self, repository: T_Repo):
        self.repository = repository

    async def get_by_id(self, _id: int) -> T_Entity | None:
        return await self.repository.get_by_id(_id)

    async def exists_by_id(self, _id: int) -> bool:
        return await self.repository.exists_by_id(_id)

    async def get_all(self, _filter: T_Filter) -> list[T_Entity]:
        return await self.repository.get_all(_filter)

    async def delete(self, entity: T_Entity):
        await self.repository.delete(entity)
