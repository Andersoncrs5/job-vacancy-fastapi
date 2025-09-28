from app.configs.db.database import EmployeeEnterpriseEntity
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter
from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import EmployeeEnterpriseEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.employee_enterprise_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime
from app.services.providers.employee_enterprise_service_provider import EmployeeEnterpriseServiceProvider

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/employee-enterprise",
    tags=["Employee Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/{employee_id}",
    response_model=ResponseBody[EmployeeEnterpriseOUT],
    status_code=200
)
async def patch(
    employee_id: int,
    dto: UpdateEmployeeEnterpriseDTO,
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if employee_id <= 0:
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
        
        employee = await employee_enterprise_service.get_by_id(employee_id)
        if employee is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Employee not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        empl_updated = await employee_enterprise_service.update(employee, dto)

        out = empl_updated.to_out()

        return ORJSONResponse(
                status_code=200,
                content=dict(ResponseBody[dict](
                    code=200,
                    message="Employee updated with successfully",
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
    "/{employee_id}",
    response_model=ResponseBody[EmployeeEnterpriseOUT],
    status_code=200,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400,
        403: RESPONSE_403,
    }
)
async def delete(
    employee_id: int,
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if employee_id <= 0:
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
        
        employee = await employee_enterprise_service.get_by_id(employee_id)
        if employee is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Employee not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await employee_enterprise_service.delete(employee)
        
        return ORJSONResponse(
                status_code=200,
                content=dict(ResponseBody[None](
                    code=200,
                    message="Employee deleted with successfully",
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
    "/{employee_id}",
    response_model=ResponseBody[EmployeeEnterpriseOUT],
    status_code=200
)
async def get_by_id(
    employee_id: int,
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if employee_id <= 0:
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
        
        employee = await employee_enterprise_service.get_by_id(employee_id)
        if employee is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Employee not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out = employee.to_out()

        return ORJSONResponse(
                status_code=200,
                content=dict(ResponseBody[dict](
                    code=200,
                    message="Employee found with successfully",
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
    response_model=Page[EmployeeEnterpriseOUT],
    status_code=200
)
async def get_all(
    filter: EmployeeEnterpriseFilter = Depends(),
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        all: Final[list[EmployeeEnterpriseEntity]] = await employee_enterprise_service.get_all(filter)

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
    "",
    response_model=ResponseBody[EmployeeEnterpriseOUT],
    status_code=201
)
async def create(
    dto: CreateEmployeeEnterpriseDTO,
    employee_enterprise_service: EmployeeEnterpriseServiceProvider = Depends(get_employee_enterprise_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        
        if user_id == dto.user_id:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You cannot add yourself",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        enterprise = await enterprise_service.get_by_user_id(user_id)
        if enterprise is None :
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

        user: Final[UserEntity | None] = await user_service.get_by_id(dto.user_id)
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

        check_exists_user: Final[bool] = await employee_enterprise_service.exists_by_user_id(dto.user_id)
        if check_exists_user == True:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="User already exists",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        employee_created: Final[EmployeeEnterpriseEntity] = await employee_enterprise_service.create(user.id, enterprise.id, dto)

        out: Final[EmployeeEnterpriseOUT] = employee_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Employee created with successfully",
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

add_pagination(router)