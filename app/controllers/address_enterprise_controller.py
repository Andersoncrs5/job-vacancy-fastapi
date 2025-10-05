from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import AddressEnterpriseEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.address_enterprise_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.services.providers.address_enterprise_service_provider import AddressEnterpriseServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/address-enterprise", 
    tags=["Address Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/toggle/status/is-public",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        404: RESPONSE_404,
        400: RESPONSE_400,
    }
)
async def patch_toggle_status_is_public(
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        enterprise = await enterprise_service.get_by_user_id(user_id)
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

        address: Final = await address_service.get_by_enterprise_id(enterprise.id)
        if address is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Address not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await address_service.toggle_is_public(address)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Address status is public changed with successfully",
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
    "/{enterprise_id}/exists",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def exists_by_id(
    enterprise_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if enterprise_id <= 0:
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

        exists: Final = await address_service.exists_by_enterprise_id(enterprise_id)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                message="",
                code=status.HTTP_200_OK,
                status=True,
                body=exists,
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
    "",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        404: RESPONSE_404,
        400: RESPONSE_400,
    }
)
async def patch(
    dto: UpdateAddressEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        enterprise = await enterprise_service.get_by_user_id(user_id)
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

        address: Final = await address_service.get_by_enterprise_id(enterprise.id)
        if address is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Address not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        address_updated = await address_service.update(address, dto)

        out = address_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Address updated with successfully",
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
    "",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        404: RESPONSE_404,
        400: RESPONSE_400,
    }
)
async def delete(
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        enterprise = await enterprise_service.get_by_user_id(user_id)
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

        address: Final = await address_service.get_by_enterprise_id(enterprise.id)
        if address is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Address not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await address_service.delete(address)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Address deleted with successfully",
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
    "/{enterprise_id}",
    status_code=200,
    response_model=ResponseBody[None],   
    responses={
        404: RESPONSE_404_CATEGORY,
        400: RESPONSE_400_ID_REQUIRED,
    }
)
async def get_by_id(
    enterprise_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if enterprise_id <= 0:
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

        address: Final = await address_service.get_by_enterprise_id(enterprise_id)
        if address is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Address not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if not address.is_public:
            return ORJSONResponse(
                status_code=403,
                content=dict(ResponseBody[None](
                    code=403,
                    message="Address display blocked by enterprise",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out = address.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Address found with successfully",
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

@router.post(
    '',
    status_code=200,
    response_model=ResponseBody[AddressEnterpriseOUT],   
    responses={
        404: RESPONSE_404,
    }
)
async def create(
    dto: CreateAddressEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    address_service: AddressEnterpriseServiceProvider = Depends(get_address_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        enterprise = await enterprise_service.get_by_user_id(user_id)
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

        address: Final = await address_service.exists_by_enterprise_id(enterprise.id)
        if address:
            return ORJSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=dict(ResponseBody[None](
                    code=status.HTTP_403_FORBIDDEN,
                    message="Address already exists",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )
 
        address_created: Final[AddressEnterpriseEntity] = await address_service.create(enterprise.id, dto)

        address_mapped: Final = address_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Address created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=dict(address_mapped),
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