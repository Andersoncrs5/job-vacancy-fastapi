from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import MySkillEntity
from app.dependencies.service_dependency import *
from app.schemas.my_skill_schemas import *
from app.utils.filter.my_skill_filter import MySkillFilter
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/my-skill", 
    tags=["MySkill"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    '/{skill_int}/exists',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody,
    responses = {
        404: RESPONSE_404
    }
)
async def exists(
    skill_int: int,
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if skill_int <= 0:
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
        
        my: Final[bool] = await my_skill_service.exists_by_skill_id_and_user_id(skill_int, user_id)
        
        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[bool](
                message="",
                code=200,
                status=True,
                body=my,
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
    '/{skill_int}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody,
    responses = {
        404: RESPONSE_404
    }
)
async def get(
    skill_int: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if skill_int <= 0:
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
        
        my: Final[MySkillEntity | None] = await my_skill_service.get_by_skill_id_and_user_id(skill_int, user_id)
        if my is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"My Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out: Final[MySkillOUT] = my.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="My Skill found with successfully",
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
    '',
    status_code = status.HTTP_200_OK,
    response_model = Page[MySkillOUT],
)
async def get_all(
    filter: MySkillFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        all: Final[list[MySkillEntity]] = await my_skill_service.get_all(filter)

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

@router.patch(
    "/{skill_id}",
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody[MySkillOUT],
    responses = {
        409: RESPONSE_409,
        400: RESPONSE_400,
        404: RESPONSE_404,
    }
)
async def update(
    skill_id: int,
    dto: UpdateMySkillDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if skill_id <= 0:
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
        
        my_skill: Final[MySkillEntity | None] = await my_skill_service.get_by_skill_id_and_user_id(skill_id, user_id)
        if my_skill is None:
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message="My Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check = await user_service.exists_by_id(user_id)
        if not check:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        my_skill_updated = await my_skill_service.update(my_skill, dto)

        out: Final[MySkillOUT] = my_skill_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="My Skill updated with successfully",
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
    '/{skill_int}',
    status_code = status.HTTP_200_OK,
    response_model = ResponseBody,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete(
    skill_int: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if skill_int <= 0:
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
        
        my: Final[MySkillEntity | None] = await my_skill_service.get_by_skill_id_and_user_id(skill_int, user_id)
        if my is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"My Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await my_skill_service.delete(my)

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody(
                message="My Skill removed with successfully",
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
    status_code = status.HTTP_201_CREATED,
    response_model = ResponseBody[MySkillOUT],
    responses = {
        409: RESPONSE_409,
        404: RESPONSE_404
    }
)
async def create(
    dto: CreateMySkillDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    my_skill_service: MySkillServiceProvider = Depends(get_my_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        check_my_skill_exists = await my_skill_service.exists_by_skill_id_and_user_id(dto.skill_id, user_id)
        if check_my_skill_exists:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody(
                    code=409,
                    message="Skill already was added",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check = await user_service.exists_by_id(user_id)
        if not check:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check_skill = await skill_service.exists_by_id(dto.skill_id)
        if not check_skill:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Skill not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        my_skill_created = await my_skill_service.create(user_id, dto)

        out: Final[MySkillOUT] = my_skill_created.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="My Skill created with successfully",
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