from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import ReviewEnterprise, UserEntity, EnterpriseEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.review_enterprise_schemas import *
from app.services.providers.skill_service_provider import SkillServiceProvider
from app.services.providers.my_skill_service_provider import MySkillServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime, timedelta
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter
import json

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/review-enterprise", 
    tags=["Review Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/{view_id}",
    response_model=ResponseBody[ReviewEnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
    }
)
async def patch(
    view_id: int,
    dto: UpdateReviewEnterpriseDTO,
    review_enterprise_service: ReviewEnterpriseServiceProvider = Depends(get_review_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
):
    if view_id <= 0:
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

        view = await review_enterprise_service.get_by_id(view_id)
        if view is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Review not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        if datetime.now(view.created_at.tzinfo) - view.created_at > timedelta(days=7):
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="You cannot update a review after 7 days of creation",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        view_updated = await review_enterprise_service.update(view, dto)

        out = view_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Review updated with successfully",
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
    "/{view_id}",
    response_model=ResponseBody[ReviewEnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
    }
)
async def delete(
    view_id: int,
    review_enterprise_service: ReviewEnterpriseServiceProvider = Depends(get_review_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
):
    if view_id <= 0:
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

        view = await review_enterprise_service.get_by_id(view_id)
        if view is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Review not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        await review_enterprise_service.delete(view)

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[None](
                message="Review deleted with successfully",
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
    "/{view_id}",
    response_model=ResponseBody[ReviewEnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
    }
)
async def get_by_id(
    view_id: int,
    review_enterprise_service: ReviewEnterpriseServiceProvider = Depends(get_review_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
):
    if view_id <= 0:
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

        view = await review_enterprise_service.get_by_id(view_id)
        if view is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Review not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        out = view.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Review found with successfully",
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
    "",
    response_model=ResponseBody[ReviewEnterpriseOUT],
    status_code=201,
    responses = {
        403: RESPONSE_403,
        404: RESPONSE_404,
        409: RESPONSE_409,
    }
)
async def create(
    dto: CreateReviewEnterpriseDTO,
    review_enterprise_service: ReviewEnterpriseServiceProvider = Depends(get_review_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        check_exists_employee = await employee_enterprise_service.exists_by_user_id(user_id)
        if check_exists_employee == False:
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message="you are not or were not an employee",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )
        
        enterprise: Final[EnterpriseEntity | None] = await enterprise_service.get_by_id(dto.enterprise_id)
        if enterprise == None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody[None](
                    code=404,
                    message=f"Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id == enterprise.user_id:
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody[None](
                    code=403,
                    message="You cannot add a review in your enterprise",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

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

        check_exists_review: Final[bool] = await review_enterprise_service.exists_by_user_id(user_id)
        if check_exists_review == True:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You already have a review to this enterprise",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )
        
        review_created: Final[ReviewEnterprise] = await review_enterprise_service.create(user_id, dto)

        out: Final[ReviewEnterpriseOUT] = review_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Review created with successfully",
                code=status.HTTP_201_CREATED,
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
    "",
    response_model=Page[ReviewEnterpriseOUT],
    status_code=200
)
async def get_all(
    filter: ReviewEnterpriseFilter = Depends(),
    review_enterprise_service: ReviewEnterpriseServiceProvider = Depends(get_review_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        all: Final[list[ReviewEnterprise]] = await review_enterprise_service.get_all(filter)

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