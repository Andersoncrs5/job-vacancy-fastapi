from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import PostEnterpriseEntity, EnterpriseEntity, CategoryEntity
from app.configs.db.enums import NotificationTypeEnum
from app.dependencies.service_dependency import *
from app.schemas.post_enterprise_schemas import *
from app.utils.enums.sum_red import SumRedEnum, ColumnEnterpriseMetricEnum, ColumnsPostEnterpriseMetricEnum
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/post-enterprise", 
    tags=["PostEnterprise"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "/{post_id}/metric",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostEnterpriseOUT],
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
    }
)
async def get_metric(
    post_id: int,
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="id is required",
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

        post: Final[PostEnterpriseEntity | None] = await post_enterprise_service.get_by_id(post_id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        metric = await post_enterprise_metric_service.get_by_id(post_id)

        out = metric.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Post metric found with successfully",
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

@router.put(
    '/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostEnterpriseOUT],
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def update(
    post_id: int,
    dto: UpdatePostEnterpriseDTO,
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Post user id is required",
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

        post: Final[PostEnterpriseEntity | None] = await post_enterprise_service.get_by_id(post_id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        post_updated: Final[PostEnterpriseEntity] = await post_enterprise_service.update(post, dto)

        post_out: Final[PostEnterpriseOUT] = post_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Post updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(post_out),
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
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostEnterpriseOUT],
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
    }
)
async def delete(
    post_id: int,
    enterprise_metric_service: EnterpriseMetricServiceProvider = Depends(get_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="id is required",
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

        post: Final[PostEnterpriseEntity | None] = await post_enterprise_service.get_by_id(post_id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        await post_enterprise_service.delete(post)

        await enterprise_metric_service.update_metric(post.enterprise_id, ColumnEnterpriseMetricEnum.post_count,
                                                      SumRedEnum.RED)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message="Post deleted with successfully",
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
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostEnterpriseOUT],
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
    }
)
async def get(
    post_id: int,
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="id is required",
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

        post: Final[PostEnterpriseEntity | None] = await post_enterprise_service.get_by_id(post_id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        await post_enterprise_metric_service.update_metric(post.id, ColumnsPostEnterpriseMetricEnum.views_count, SumRedEnum.SUM)
        post_out: Final[PostEnterpriseOUT] = post.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Post found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(post_out),
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
    status_code=status.HTTP_200_OK,
    response_model=Page[PostEnterpriseOUT],
    )
async def get_all(
    filter: PostEnterpriseFilter = Depends(),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        all: Final[list[PostEnterpriseEntity]] = await post_enterprise_service.get_all(filter)

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

@router.post(
    '/{category_id}',
    response_model=ResponseBody[PostEnterpriseOUT],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def create(
    category_id: int,
    dto: CreatePostEnterpriseDTO,
    enterprise_metric_service: EnterpriseMetricServiceProvider = Depends(get_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    notification_service: NotificationEventServiceProvider = Depends(get_notification_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        enter: Final[EnterpriseEntity | None] = await enterprise_service.get_by_user_id(user_id)
        if enter is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
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
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        if not category.is_active:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
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

        await category_service.sum_red_post_count(
            category,
            SumRedEnum.SUM
        )

        await enterprise_metric_service.update_metric(
            post_enterprise_created.enterprise_id,
            ColumnEnterpriseMetricEnum.post_count,
            SumRedEnum.SUM
        )

        await notification_service.notify_event_to_kafka(
            entity_id=post_enterprise_created.id,
            actor_id=enter.id,
            _type=NotificationTypeEnum.NEW_POST_ENTERPRISE,
            data = {
                "actor_name": enter.name
            },
        )

        await post_enterprise_metric_service.create(post_enterprise_created.id)
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