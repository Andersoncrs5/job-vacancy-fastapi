from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import VacancyEntity, UserEntity, SkillEntity, VacancySkillEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.schemas.vacancy_skill_schemas import VacancySkillOUT
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.vacancy_schemas import *
from app.services.providers.vacancy_service_provider import VacancyServiceProvider
from app.services.providers.vacancy_skill_service_provider import VacancySkillServiceProvider
from app.services.providers.skill_service_provider import SkillServiceProvider
from app.dependencies.service_dependency import *
from app.schemas.vacancy_skill_schemas import CreateVacancySkillDTO, UpdateVacancySkillDTO
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime
import uuid

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/vacancy-skill", 
    tags=["Vacancy Skill"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/{id}",
    response_model=ResponseBody[None],
    status_code = 200,
    responses = {
        404: RESPONSE_404
    }
)
async def patch(
    id: int,
    dto: UpdateVacancySkillDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    vacancy_skill_service: VacancySkillServiceProvider = Depends(get_vacancy_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody[None](
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final[bool] = await user_service.exists_by_id(user_id)
        if user == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        vs = await vacancy_skill_service.get_by_id(id)
        if vs == None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        vs_updated = await vacancy_skill_service.update(vs, dto)
        
        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[None](
                message="Skill details updated with successfully",
                code=200,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )


@router.get(
    "/{vacancy_id}/all",
    status_code=status.HTTP_200_OK,
    response_model=Page[VacancySkillOUT]
)
async def get_all(
    vacancy_id: int,
    vacancy_service: VacancyServiceProvider = Depends(get_vacancy_service_provider_dependency),
    vacancy_skill_service: VacancySkillServiceProvider = Depends(get_vacancy_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if vacancy_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody[None](
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        exists_vacancy = await vacancy_service.exists_by_id(vacancy_id)
        if exists_vacancy == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Vacancy not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        all: Final = await vacancy_skill_service.get_all(vacancy_id)

        return paginate(all)

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

@router.delete(
    "/{id}",
    response_model=ResponseBody[VacancyOUT],
    status_code = 200,
    responses = {
        404: RESPONSE_404
    }
)
async def delete(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    vacancy_skill_service: VacancySkillServiceProvider = Depends(get_vacancy_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody[None](
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final[bool] = await user_service.exists_by_id(user_id)
        if user == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        vs = await vacancy_skill_service.get_by_id(id)
        if vs == None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await vacancy_skill_service.delete(vs)
        
        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[None](
                message="Skill removed with successfully",
                code=200,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

@router.post(
    "",
    response_model=ResponseBody[int],
    status_code=201,
    responses = {
        404: RESPONSE_404,
        403: RESPONSE_403,
    }
)
async def create(
    dto: CreateVacancySkillDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    vacancy_service: VacancyServiceProvider = Depends(get_vacancy_service_provider_dependency),
    vacancy_skill_service: VacancySkillServiceProvider = Depends(get_vacancy_skill_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final[bool] = await user_service.exists_by_id(user_id)
        if user == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        exists_vs = await vacancy_skill_service.exists_by_vacancy_id_and_skill_id(dto.vacancy_id, dto.skill_id)
        if exists_vs:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Skill already was added",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        skill: Final[SkillEntity | None] = await skill_service.get_by_id(dto.skill_id)
        if skill is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        vacancy: Final[VacancyEntity | None] = await vacancy_service.get_by_id(dto.vacancy_id)
        if vacancy is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Vacancy not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        skill_added_in_vacancy = await vacancy_skill_service.create(dto)

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[int](
                code=201,
                message=f"Skill added with sucessfully",
                status=True,
                body=skill_added_in_vacancy.id,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

add_pagination(router)