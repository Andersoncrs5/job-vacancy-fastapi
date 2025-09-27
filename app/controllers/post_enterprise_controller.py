from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import PostEnterpriseEntity, EnterpriseEntity, CategoryEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.enums.sum_red import SumRedEnum
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.post_enterprise_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.services.providers.post_enterprise_service_provider import PostEnterpriseServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/post-enterprise", 
    tags=["PostEnterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()


@router.post(
    '/{category_id}',
    response_model=ResponseBody[PostEnterpriseOUT],
    status_code=status.HTTP_201_CREATED,
    responses={
        404: RESPONSE_404_USER,
        404: RESPONSE_404_CATEGORY,
    }
)
async def create(
    category_id: int,
    dto: CreatePostEnterpriseDTO,
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
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

        enter: Final[EnterpriseEntity | None] = await enterprise_service.get_by_user_id(user_id)
        if enter is None:
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
        
        if category.is_active == False:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Category are not actived",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        post_enterprise_created: Final[PostEnterpriseEntity] = await post_enterprise_service.create(enter.id, category.id, dto)

        await category_service.sum_red_post_count(category, SumRedEnum.SUM)

        post_enterprise_out = post_enterprise_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Post created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=dict(post_enterprise_out),
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