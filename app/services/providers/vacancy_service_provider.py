from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.configs.db.database import VacancyEntity
from app.repositories.providers.area_repository_provider import AreaRepositoryProvider
from app.repositories.providers.vacancy_repository_provider import VacancyRepositoryProvider
from app.schemas.vacancy_schemas import CreateVacancyDTO, UpdateVacancyDTO
from app.services.base.vacancy_service_base import VacancyServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.vacancy_filter import VacancyFilter
from app.utils.res.response_body import ResponseBody


class VacancyServiceProvider(
    VacancyServiceBase,
    GenericService[
        VacancyEntity,
        VacancyRepositoryProvider,
        VacancyFilter
    ]
):
    def __init__(self, repository: VacancyRepositoryProvider, area_repo: AreaRepositoryProvider):
        super().__init__(repository)
        self.area_repository = area_repo

    async def update(self, vacancy: VacancyEntity, dto: UpdateVacancyDTO) -> VacancyEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(vacancy, field, value)

        if dto.area_id is not None:
            check = await self.area_repository.exists_by_id(dto.area_id)

            if not check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=dict(ResponseBody(
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

    async def create(self, enterprise_id: int, dto: CreateVacancyDTO) -> VacancyEntity:
        vacancy = dto.to_entity()
        vacancy.enterprise_id = enterprise_id

        return await self.repository.add(vacancy)