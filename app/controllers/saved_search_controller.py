from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import SavedSearchEntity
from app.dependencies.service_dependency import *
from app.schemas.saved_search_schemas import *
from app.utils.filter.saved_search_filter import SavedSearchFilter
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/saved-search", 
    tags=["Saved Search"],
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
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        404: RESPONSE_404
    }
)
async def patch_by_id(
    id: int,
    dto: UpdateSavedSearchDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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
        
        save: Final[SavedSearchEntity | None] = await saved_search_service.get_by_id(id)
        
        if save is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Search not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id != save.user_id :
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody(
                    code=403,
                    message=f"You cannot to update this search",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        save_updated = await saved_search_service.update(save, dto)

        out = save_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Search updated with successfully",
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
    '/{id}/toggle/status/is-public',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        403: RESPONSE_403,
        404: RESPONSE_404
    }
)
async def toggle_is_public(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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
        
        save: Final[SavedSearchEntity | None] = await saved_search_service.get_by_id(id)
        if save is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Search not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id != save.user_id :
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody(
                    code=403,
                    message=f"You cannot to change status this search",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        save_updated = await saved_search_service.toggle_is_public(save)

        out: Final = save_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Search changed status public with successfully",
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
    '/{id}/toggle/status/notifications-enabled',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        403: RESPONSE_403,
        404: RESPONSE_404
    }
)
async def toggle_notifications_enabled(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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
        
        save: Final[SavedSearchEntity | None] = await saved_search_service.get_by_id(id)
        if save is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Search not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id != save.user_id :
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody(
                    code=403,
                    message=f"You cannot to change status this search",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        save_updated = await saved_search_service.toggle_notifications_enabled(save)

        out: Final = save_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Search changed status notifications enabled with successfully",
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
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        403: RESPONSE_403,
        404: RESPONSE_404
    }
)
async def delete_by_id(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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
        
        save: Final[SavedSearchEntity | None] = await saved_search_service.get_by_id(id)
        if save is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Search not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id != save.user_id :
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody(
                    code=403,
                    message=f"You cannot to delete this search",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await saved_search_service.delete(save)

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody(
                message="Search deleted with successfully",
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
    '',
    status_code = status.HTTP_200_OK,
    response_model = Page[SavedSearchOUT],
)
async def get_all(
    filter: SavedSearchFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)
        
        all: Final = await saved_search_service.get_all(filter)

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

@router.get(
    '/{id}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        404: RESPONSE_404
    }
)
async def get_by_id(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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
        
        save: Final[SavedSearchEntity | None] = await saved_search_service.get_by_id(id)
        if save is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Search not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out: Final = save.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Search found with successfully",
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

@router.post(
    '',
    status_code = status.HTTP_201_CREATED,
    response_model = ResponseBody[SavedSearchOUT],
    responses = {
        404: RESPONSE_404
    }
)
async def create(
    dto: CreateSavedSearchDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    saved_search_service = Depends(get_saved_search_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        exists = await user_service.exists_by_id(user_id)
        if not exists:
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    message="User not found",
                    code=404,
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        search: Final[SavedSearchEntity] = await saved_search_service.create(user_id, dto)
        
        out: Final = search.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Search found with successfully",
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

add_pagination(router)