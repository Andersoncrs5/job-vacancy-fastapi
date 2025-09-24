from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import CategoryEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.category_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.category_filter import CategoryFilter
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/category", 
    tags=["Category"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoryOUT],
)
async def get_all(
    category_filter: CategoryFilter = Depends(),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
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

        categories: Final[list[CategoryEntity]] = await category_service.get_all_filter(True, category_filter)

        return paginate(categories)

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
    '/{category_id}/toggle/status/is_active',
    status_code=200,
    response_model=ResponseBody[CategoryOUT],   
    responses={
        404: RESPONSE_404_CATEGORY,
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def toggle_change_is_status(
    category_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        category: Final[CategoryEntity | None] = await category_service.get_by_id(category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        category_updated: Final[CategoryEntity] = await category_service.toggle_is_active(category)

        category_mapped: Final[CategoryOUT] = category_updated.to_category_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Category status changed with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(category_mapped),
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

@router.put(
    '/{category_id}',
    status_code=200,
    response_model=ResponseBody[CategoryOUT],   
    responses={
        404: RESPONSE_404_CATEGORY,
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def update(
    category_id: int,
    dto: UpdateCategoryDTO,
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        category: Final[CategoryEntity | None] = await category_service.get_by_id(category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if dto.name != None and dto.name != category.name:
            check: Final[bool] = await category_service.exists_by_name(dto.name)
            if check:
                return ORJSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_409_CONFLICT,
                        message=f"Name {dto.name} already in use",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )

            category.name = dto.name

        if dto.slug != None and dto.slug != category.slug:
            check_slug: Final[bool] = await category_service.exists_by_slug(dto.slug)
            if check_slug:
                return ORJSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_409_CONFLICT,
                        message=f"Slug {dto.slug} already in use",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version = 1,
                        path = None
                    ))
                )

            category.slug = dto.slug

        category_updated: Final[CategoryEntity] = await category_service.update(category, dto)

        category_mapped: Final[CategoryOUT] = category_updated.to_category_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Category updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(category_mapped),
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
    "/{category_id}",
    status_code=200,
    response_model=ResponseBody[CategoryOUT],   
    responses={
        404: RESPONSE_404_CATEGORY,
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def get_by_id(
    category_id: int,
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        category: Final[CategoryEntity | None] = await category_service.get_by_id(category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        category_mapped: Final[CategoryOUT] = category.to_category_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Category found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(category_mapped),
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
    "/{category_id}",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        404: RESPONSE_404_CATEGORY,
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def delete(
    category_id: int,
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        category: Final[CategoryEntity | None] = await category_service.get_by_id(category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await category_service.delete(category)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Category deleted with successfully",
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
    status_code=200,
    response_model=ResponseBody[CategoryOUT],   
    responses={
        400: RESPONSE_400,
    }
)
async def create(
    dto: CreateCategoryDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
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

        check_name: Final[bool] = await category_service.exists_by_name(dto.name)
        if check_name == True:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Category name: {dto.name} already exists",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check_slug: Final[bool] = await category_service.exists_by_slug(dto.slug)
        if check_slug == True:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Category slug: {dto.slug} already exists",
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
 
        category_created: Final[CategoryEntity] = await category_service.create(user, dto)

        category_mapped: Final[CategoryOUT] = category_created.to_category_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Category created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=dict(category_mapped),
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