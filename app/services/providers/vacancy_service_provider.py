from app.services.base.vacancy_service_base import VacancyServiceBase
from app.repositories.providers.vacancy_repository_provider import VacancyRepositoryProvider
from app.repositories.providers.area_repository_provider import AreaRepositoryProvider
from typing import Final
from fastapi import HTTPException, status
from app.utils.res.response_body import ResponseBody
from datetime import datetime
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import List
from app.schemas.vacancy_schemas import CreateVacancyDTO, UpdateVacancyDTO

class VacancyServiceProvider(VacancyServiceBase):
    def __init__(self, repository: VacancyRepositoryProvider, area_repo: AreaRepositoryProvider):
        self.repository = repository
        self.area_repository = area_repo
    
    async def delete(self, vacancy: VacancyEntity):
        await self.repository.delete(vacancy)

    async def update(self, vacancy: VacancyEntity, dto: UpdateVacancyDTO) -> VacancyEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(vacancy, field, value)

        if dto.area_id != None:
            check = await self.area_repository.exists_by_id(dto.area_id)

            if check == False:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=dict(ResponseBody[None](
                        code = status.HTTP_404_NOT_FOUND,
                        message = f"Area not found",
                        body=None,
                        path=None,
                        status=False,
                        timestamp=str(datetime.now()),
                        version=1
                    ))
                )

            vacancy.area_id = dto.area_id

        return await self.repository.save(vacancy)

    async def get_all(self, filter: VacancyFilter) -> List[VacancyEntity]:
        return await self.repository.get_all(filter)
    
    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def get_by_id(self, id: int) -> VacancyEntity | None:
        return await self.repository.get_by_id(id)

    async def create(self, enterprise_id: int, dto: CreateVacancyDTO) -> VacancyEntity:
        vacancy = dto.to_entity()
        vacancy.enterprise_id = enterprise_id

        return await self.repository.add(vacancy)