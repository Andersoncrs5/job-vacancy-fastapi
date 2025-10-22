import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.utils.filter.roles_filter import RolesFilter
from app.utils.res.responses_http import *
from app.dependencies.service_dependency import *

load_dotenv()

ROLE_SUPER_ADM: Final[str] = os.getenv("ROLE_SUPER_ADM")
ROLE_ADM: Final[str] = os.getenv("ROLE_ADM")
ROLE_MASTER: Final[str] = os.getenv("ROLE_MASTER")

URL = "/api/v1/adm"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Adm"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.post(
    "/toggle/{email}/{role_title}",
    response_model=ResponseBody,
    status_code=status.HTTP_200_OK
)
async def impl_role_in_user(
    email: str,
    role_title: str,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    my_roles_service: MyRolesServiceProvider = Depends(get_my_role_provider_dependency),
    roles_service: RolesServiceProvider = Depends(get_role_provider_dependency),
    jwt_service: JwtServiceProvider = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        jwt_service.check_master(token)

        if not (role_title in [ROLE_SUPER_ADM, ROLE_ADM]):
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message=f"The role {role_title} is not {ROLE_SUPER_ADM} or {ROLE_ADM}",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        user = await user_service.get_by_email(email=email)
        if not user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message=f"User not found with email: {email}",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        role = await roles_service.get_by_title(role_title)
        if not role:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message=f"Role not found with name: {role_title}",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        check = await my_roles_service.get_by_user_id_and_role_id(
            user_id=user.id,
            role_id=role.id
        )

        if check is not None:
            await my_roles_service.delete(check)

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    message=f"User {user.name} not a more a {role_title.lower()}",
                    code=status.HTTP_200_OK,
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await my_roles_service.create(
            user_id=user.id,
            role_id=role.id,
        )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message=f"User {user.name} now is a {role_title.lower()}",
                code=status.HTTP_200_OK,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        print("\n\n")
        print(e)
        print("\n\n")
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

