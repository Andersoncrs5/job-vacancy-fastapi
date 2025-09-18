from fastapi import APIRouter, Depends, status
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from fastapi.responses import JSONResponse
from app.configs.db.database import UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.tokens import Tokens
from app.utils.res.responses_http import *
from app.schemas.user_schemas import CreateUserDTO
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from datetime import datetime
from app.services.providers.crypto_service import verify_password

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/auth", 
    tags=["Auth"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "/{refresh_token}",
    status_code=200,
    response_model=ResponseBody[Tokens],
    responses={
        404: RESPONSE_404_USER
    }
)
async def refresh_token_method(
    refresh_token: str,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    ):
    
    check_token = jwt_service.decode_token(refresh_token)
    if check_token is None:
        return JSONResponse(
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

    user_id: Final[int | None] = jwt_service.extract_user_id(refresh_token)
    if user_id is None:
        return JSONResponse(
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

    user: Final[UserEntity | None] = await user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="You are not authorized",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    token: Final[str] = jwt_service.create_access_token(user)
    new_refresh_token: Final[str] = jwt_service.create_refresh_token(user)

    await user_service.set_refresh_token(new_refresh_token, user)

    tokens: Final[Tokens] = Tokens(
        token=token, 
        refresh_token=refresh_token,
        exp_token = None,
        exp_refresh_token = None
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(ResponseBody[dict](
            message="New Tokens sended",
            code=status.HTTP_200_OK,
            status=True,
            body=dict(tokens),
            timestamp=str(datetime.now()),
            version = 1,
            path = None
        ))
    )

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[Tokens],
    description="endpoint to login user",
)
async def login(
    dto: LoginDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency)
):
    user: Final[UserEntity | None] = await user_service.get_by_email(dto.email)
    if user is None:
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    if verify_password(dto.password,user.password) == False :
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    token: Final[str] = jwt_service.create_access_token(user)
    refresh_token: Final[str] = jwt_service.create_refresh_token(user)

    await user_service.set_refresh_token(refresh_token, user)

    tokens: Final[Tokens] = Tokens(
        token=token, 
        refresh_token=refresh_token,
        exp_token = None,
        exp_refresh_token = None
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(ResponseBody[dict](
            message="Welcome again",
            code=status.HTTP_200_OK,
            status=True,
            body=dict(tokens),
            timestamp=str(datetime.now()),
            version = 1,
            path = None
        ))
    )


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[Tokens],
    description="endpoint to register new user",
    responses={
        409: {
           "model": ResponseBody[None],
           "description": "Email already exists"
        }
    }
)
async def resgiter(
    dto: CreateUserDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency)
):
    check: Final[bool] = await user_service.exists_by_email(dto.email)
    if check :
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=dict(ResponseBody[None](
                code=status.HTTP_409_CONFLICT,
                message="Email already in use",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    user_created: Final[UserEntity] = await user_service.create(dto)

    token: Final = jwt_service.create_access_token(user_created)
    refresh_token: Final = jwt_service.create_refresh_token(user_created)

    await user_service.set_refresh_token(refresh_token, user_created)

    tokens: Final[Tokens] = Tokens(
        token=token, 
        refresh_token=refresh_token,
        exp_token = None,
        exp_refresh_token = None
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(ResponseBody[dict](
            message="Welcome",
            code=201,
            status=True,
            body=dict(tokens),
            timestamp=str(datetime.now()),
            path = None,
            version = 1
        ))
    )