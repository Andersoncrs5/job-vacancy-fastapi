from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.commands.command_linner import ROLE_SUPER_ADM, ROLE_ADM, ROLE_USER, ROLE_MASTER
from app.configs.db.enums import NotificationTypeEnum
from app.schemas.user_roles_schemas import UserRolesOUT
from app.utils.filter.my_role_filter import MyRolesFilter
from app.utils.filter.roles_filter import RolesFilter
from app.utils.res.responses_http import *
from app.dependencies.service_dependency import *

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
    notification_service: NotificationEventServiceProvider = Depends(get_notification_service_provider_dependency),
    roles_service: RolesServiceProvider = Depends(get_role_provider_dependency),
    jwt_service: JwtServiceProvider = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        auth: bool = jwt_service.check_authorization_boolean_style(token, [ROLE_MASTER])
        if not auth:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody(
                    code=status.HTTP_401_UNAUTHORIZED,
                    message=f"You cannot access this route",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if not (role_title in [ROLE_SUPER_ADM, ROLE_ADM, ROLE_USER]):
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

            await notification_service.notify_user_about(
                entity_id=None,
                actor_id=user.id,
                _type=NotificationTypeEnum.SYSTEM,
                data={
                    "status": True,
                    "title": f"Role {check.role.title} Removed",
                    "content": (
                        f"Please be advised that your **{check.role.title}** role has been removed from your profile. "
                        f"We appreciate the time and dedication you showed while serving in this capacity. "
                        f"You still have regular access to the system."
                    )
                }
            )

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

        role_added = await my_roles_service.create(
            user_id=user.id,
            role_id=role.id,
        )

        await notification_service.notify_user_about(
            entity_id=None,
            actor_id=user.id,
            _type=NotificationTypeEnum.SYSTEM,
            data={
                "status": True,
                "title": f"Congratulations! You are the new {role_added.role.title}",
                "content": (
                    f"Congratulations! You have just been assigned the **{role_added.role.title}** role within the system. "
                    f"This new responsibility reflects our confidence in your dedication and collaboration for the smooth operation of the platform. "
                    f"Thank you for your contribution!"
                )
            }
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


@router.get(
    "",
    response_model=Page[UserRolesOUT],
    status_code=status.HTTP_200_OK
)
async def get_all(
    _filter: MyRolesFilter  = Depends(),
    my_roles_service: MyRolesServiceProvider = Depends(get_my_role_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        auth = jwt_service.check_authorization_boolean_style(token, [ROLE_MASTER])
        if not auth:
            return jwt_service.throw_unauthorized("You are not authorized")

        jwt_service.valid_credentials(credentials)

        _all: Final = await my_roles_service.get_all(_filter)

        return paginate(_all)
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