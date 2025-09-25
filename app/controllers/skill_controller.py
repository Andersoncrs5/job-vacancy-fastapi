from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import SkillEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.skill_schemas import *
from app.services.providers.skill_service_provider import SkillServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/skill", 
    tags=["Skill"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.post(
    '',
    status_code = status.HTTP_201_CREATED,
    response_model = ResponseBody[SkillOUT]
)
async def create(
    dto: CreateSkillDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    skill_service: SkillServiceProvider = Depends(get_skill_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)
        
        check: Final[bool] = await skill_service.exists_by_name(dto.name)
        if check == True :
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message=f"Skill name {dto.name} already exists",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        skill_created: Final[SkillEntity] = await skill_service.create(dto)

        out: Final[SkillOUT] = skill_created.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Skill created with successfully",
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