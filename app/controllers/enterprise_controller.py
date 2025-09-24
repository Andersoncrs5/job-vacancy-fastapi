from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import EnterpriseEntity, UserEntity, IndustryEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.enterprise_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.enterprise_filter import EnterpriseFilter
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/enterprise", 
    tags=["Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()


@router.get(
    "/{name}/exists/name",
    response_model=ResponseBody[bool],
    status_code=200,
)
async def exists_name(
    name: str,
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)

        check = await enterprise_service.exists_by_name(name)

        message = "Enterprise name already exists" if check else "Enterprise name not exists"

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                message=message,
                code=status.HTTP_200_OK,
                status=True,
                body=check,
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
    "",
    response_model=Page[EnterpriseOUT],
    status_code=200,
)
async def get_all(
    filter: EnterpriseFilter  = Depends(),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)

        all: Final = await enterprise_service.get_all_filter(filter)

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

@router.put(
    "",
    response_model=ResponseBody[EnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def update(
    dto: UpdateEnterpriseDTO,
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    industry_service: IndustryServiceProvider = Depends(get_industry_service_provider_dependency),
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

        enterprise: Final[EnterpriseEntity | None] = await enterprise_service.get_by_user_id(user_id)
        if enterprise is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )
        
        if dto.industry_id != None and dto.industry_id != enterprise.industry_id:
            check: bool = await industry_service.exists_by_id(dto.industry_id)
            if check == False:
                return ORJSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_409_CONFLICT,
                        message="Industry not exists",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )

            enterprise.industry_id = dto.industry_id

        if dto.name != None and dto.name !=  enterprise.name:
            check: bool = await enterprise_service.exists_by_name(dto.name)
            if check :
                return ORJSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_409_CONFLICT,
                        message="Enterprise name '{dto.name}' is already in use",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )
            enterprise.name = dto.name

        enterprise_updated = await enterprise_service.update(enterprise, dto)

        enterprise_out = enterprise_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Enterprise updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(enterprise_out),
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
    "",
    response_model=ResponseBody[EnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete_my_enterprise(
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
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

        enterprise: Final[EnterpriseEntity | None] = await enterprise_service.get_by_user_id(user_id)
        if enterprise is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await enterprise_service.delete(enterprise)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Enterprise deleted with successfully",
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

@router.get(
    "/my",
    response_model=ResponseBody[EnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def get_my_enterprise(
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
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

        enterprise: Final[EnterpriseEntity | None] = await enterprise_service.get_by_user_id(user_id)
        if enterprise is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        enterprise_out = enterprise.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Enterprise found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(enterprise_out),
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
    "/{id}",
    response_model=ResponseBody[EnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def get(
    id: int,
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
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

        enterprise: Final[EnterpriseEntity | None] = await enterprise_service.get_by_id(id)
        if enterprise is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        enterprise_out = enterprise.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Enterprise found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(enterprise_out),
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
    '/{industry_id}',
    response_model=ResponseBody[EnterpriseOUT],
    status_code=201,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def create(
    industry_id: int,
    dto: CreateEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    industry_service: IndustryServiceProvider = Depends(get_industry_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if industry_id <= 0:
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

        exists_by_name = await enterprise_service.exists_by_name(dto.name)
        if exists_by_name == True :
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Name {dto.name} are in use",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        exists_enterprise: Final[bool] = await enterprise_service.exists_by_user_id(user_id)
        if exists_enterprise == True :
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You already have a enterprise",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        user: Final[UserEntity | None] = await user_service.get_by_id(user_id)
        if user is None:
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

        industry: Final[IndustryEntity | None] = await industry_service.get_by_id(industry_id)
        if industry is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Industry not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        enterprise_created: Final[EnterpriseEntity] = await enterprise_service.create(industry, user, dto)

        enterprise_out: Final[EnterpriseOUT] = enterprise_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Enterprise created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=dict(enterprise_out),
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