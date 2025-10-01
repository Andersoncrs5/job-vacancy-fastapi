from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import AreaEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.area_schemas import *
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime
from app.utils.filter.area_filter import AreaFilter
from app.services.providers.area_service_provider import AreaServiceProvider

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/area", 
    tags=["Area"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    '/{id}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[AreaOUT],
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def patch(
    id: int,
    dto: UpdateAreaDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
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

        jwt_service.valid_credentials(credentials)
        
        area: Final[AreaEntity | None] = await area_service.get_by_id(id)
        if area is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Area not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        area_updated = await area_service.update(area, dto)

        out: Final[AreaOUT] = area_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Area updated with successfully",
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

@router.patch(
    '/{id}/toggle/status/is-active',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[AreaOUT],
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def toggle_status_active(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
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

        jwt_service.valid_credentials(credentials)
        
        area: Final[AreaEntity | None] = await area_service.get_by_id(id)
        if area is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Area not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        area_changed = await area_service.toggle_is_active(area)

        out: Final[AreaOUT] = area_changed.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Area status is active changed with successfully",
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

@router.delete(
    '/{id}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[AreaOUT],
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
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

        jwt_service.valid_credentials(credentials)
        
        area: Final[AreaEntity | None] = await area_service.get_by_id(id)
        if area is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Area not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await area_service.delete(area)

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[None](
                message="Area deleted with successfully",
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
    '/{id}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[AreaOUT],
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def get_by_id(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
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

        jwt_service.valid_credentials(credentials)
        
        area: Final[AreaEntity | None] = await area_service.get_by_id(id)
        if area is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Area not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out: Final[AreaOUT] = area.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Area found with successfully",
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

@router.get(
    '/{name}/exists',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[bool],
)
async def exists_by_name(
    name: str,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)
        
        check: Final = await area_service.exists_by_name(name)
        
        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[bool](
                message="",
                code=200,
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

@router.post(
    '',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[AreaOUT],
)
async def post(
    dto: CreateAreaDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service: AreaServiceProvider = Depends(get_area_service_provider_dependency),
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
        
        check_exists_name: Final[bool] = await area_service.exists_by_name(dto.name)
        if check_exists_name == True:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Name {dto.name} is in use! Try another name",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        area_created = await area_service.create(user_id, dto)

        out = area_created.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Area created with successfully",
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
    '',
    status_code = status.HTTP_200_OK,
    response_model = Page[AreaOUT],
)
async def get_all(
    filter: AreaFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    area_service: AreaServiceProvider = Depends(get_area_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)
        
        all: Final[list[AreaEntity]] = await area_service.get_all(filter)

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

add_pagination(router)