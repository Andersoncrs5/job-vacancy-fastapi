from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import CurriculumEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.curriculum_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/curriculum", 
    tags=["Curriculum"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    '/toggle/status/is_updated',
    response_model=ResponseBody[CurriculumOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def toggle_is_updated(
    curriculum_service: CurriculumServiceProvider = Depends(get_curriculum_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum = await curriculum_service.get_by_user_id(user_id)
        if curriculum is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Curriculum not found",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum_updated = await curriculum_service.toggle_status_is_updated(curriculum)

        out: Final[CurriculumOUT] = curriculum_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Curriculum status is updated changed with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(out),
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

@router.patch(
    '',
    response_model=ResponseBody[CurriculumOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def update(
    dto: UpdateCurriculumDTO,
    curriculum_service: CurriculumServiceProvider = Depends(get_curriculum_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum = await curriculum_service.get_by_user_id(user_id)
        if curriculum is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Curriculum not found",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum_updated = await curriculum_service.update(curriculum, dto)

        out: Final[CurriculumOUT] = curriculum_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Curriculum updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(out),
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

@router.delete(
    '',
    response_model=ResponseBody[CurriculumOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete(
    curriculum_service: CurriculumServiceProvider = Depends(get_curriculum_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum = await curriculum_service.get_by_user_id(user_id)
        if curriculum is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Curriculum not found",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Curriculum deleted with successfully",
                code=status.HTTP_200_OK,
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
    '',
    response_model=ResponseBody[CurriculumOUT],
    status_code=201,
    responses = {
        404: RESPONSE_404,
        409: RESPONSE_409,
        400: RESPONSE_400
    }
)
async def create(
    dto: CreateCurriculumDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    curriculum_service: CurriculumServiceProvider = Depends(get_curriculum_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum: Final[bool] = await curriculum_service.exists_by_user_id(user_id)
        if curriculum == True :
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"you already have a Curriculum",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        curriculum_created: Final[CurriculumEntity] = await curriculum_service.create(user_id, dto)

        out: Final[CurriculumOUT] = curriculum_created.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Curriculum created with successfully",
                code=201,
                status=True,
                body=dict(out),
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
    '/{user_id}',
    response_model=ResponseBody[CurriculumOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def get_by_user_id(
    user_id: int,
    curriculum_service: CurriculumServiceProvider = Depends(get_curriculum_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if user_id <= 0:
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
        jwt_service.valid_credentials(credentials)

        curriculum = await curriculum_service.get_by_user_id(user_id)
        if curriculum == None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Curriculum not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out: Final[CurriculumOUT] = curriculum.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Curriculum found with successfully",
                code=200,
                status=True,
                body=dict(out),
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