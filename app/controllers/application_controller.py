from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.dependencies.service_dependency import *
from app.schemas.application_schemas import ApplicationOUT, UpdateApplicationDTO
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnsVacancyMetricEnum
from app.utils.filter.applications_filter import ApplicationFilter
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/application",
    tags=["Application"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()


@router.patch(
    "/{id}",
    status_code=200,
    response_model=ResponseBody,
)
async def patch(
    id: int,
    dto: UpdateApplicationDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    application_service: ApplicationServiceProvider = Depends(get_application_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final = await user_service.get_by_id(user_id)
        if not user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        app = await application_service.get_by_id(id)
        if not app:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Application not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        app_updated = await application_service.update(app, dto)

        out = app_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                code=status.HTTP_200_OK,
                message="Application updated with successfully",
                status=True,
                body=dict(out),
                timestamp=str(datetime.now()),
                version=1,
                path=None
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
                version=1,
                path=None
            ))
        )

@router.delete(
    "/{id}",
    status_code=200,
    response_model=ResponseBody,
)
async def delete(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    vacancy_metric_service: VacancyMetricServiceProvider = Depends(get_vacancy_metric_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    application_service: ApplicationServiceProvider = Depends(get_application_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final = await user_service.get_by_id(user_id)
        if not user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        app = await application_service.get_by_id(id)
        if not app:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Application not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if app.user_id != user.id:
            return ORJSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=dict(ResponseBody(
                    code=status.HTTP_403_FORBIDDEN,
                    message="You are not authorized to removed this application",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.vacancy_application_count, SumRedEnum.RED)
        await vacancy_metric_service.update_metric(
            app.vacancy_id,
            ColumnsVacancyMetricEnum.applications_count,
            SumRedEnum.RED
        )
        await application_service.delete(app)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                code=status.HTTP_200_OK,
                message="Application removed with successfully",
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
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
                version=1,
                path=None
            ))
        )

@router.get(
    "",
    response_model=Page[ApplicationOUT],
    status_code=200
)
async def get_all(
    filter: ApplicationFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    application_service: ApplicationServiceProvider = Depends(get_application_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)
        entities: Final = await application_service.get_all(filter)

        return paginate(entities)

    except Exception as e:
        return ORJSONResponse(
            status_code=500,
            content=dict(ResponseBody[Any](
                code=500,
                message="Error in server! Please try again later",
                status=False,
                body=str(e),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

@router.post(
    "/{id}",
    response_model=ResponseBody[ApplicationOUT],
    responses={
        404: RESPONSE_404,
        403: RESPONSE_403,
        400: RESPONSE_400,
    }
)
async def create(
        id: int,
        user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
        vacancy_service: VacancyServiceProvider = Depends(get_vacancy_service_provider_dependency),
        user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
        vacancy_metric_service: VacancyMetricServiceProvider = Depends(get_vacancy_metric_service_provider_dependency),
        application_service: ApplicationServiceProvider = Depends(get_application_service_provider_dependency),
        jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        user: Final = await user_service.get_by_id(user_id)
        if not user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        exists_application = await application_service.exists_by_application(user_id, id)
        if exists_application:
            return ORJSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=dict(ResponseBody(
                    code=status.HTTP_409_CONFLICT,
                    message="You have already applied for this position!",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        vacancy = await vacancy_service.get_by_id(id)
        if vacancy is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Vacancy not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if vacancy.application_deadline and vacancy.application_deadline < datetime.now().date():
            return ORJSONResponse(
                status_code=400,
                content=dict(ResponseBody(
                    code=400,
                    message="Vacancy is closed",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        applied = await application_service.create(vacancy.id, user_id)
        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.vacancy_application_count,
                                                   SumRedEnum.SUM)

        await vacancy_metric_service.update_metric(vacancy.id, ColumnsVacancyMetricEnum.applications_count, SumRedEnum.SUM)

        out = applied.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Application sent successfully",
                code=201,
                status=True,
                body=dict(out),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print("Error ", e)
        return ORJSONResponse(
            status_code=500,
            content=dict(ResponseBody[Any](
                code=500,
                message="Error in server! Please try again later",
                status=False,
                body=str(e),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

add_pagination(router)