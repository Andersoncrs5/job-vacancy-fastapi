from datetime import datetime

from pydantic import Field

from app.configs.db.enums import ReactionTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.post_enterprise_schemas import PostEnterpriseOUT
from app.schemas.user_schemas import UserOUT


class ReactionPostEnterpriseSimpleDTO(ORJSONModel):
    id: int
    user_id: int
    post_enterprise_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime

class ReactionPostEnterpriseWithRelationshipDTO(ORJSONModel):
    id: int
    user_id: int
    post_enterprise_id: int
    reaction_type: ReactionTypeEnum
    user: UserOUT
    post_enterprise: PostEnterpriseOUT
    created_at: datetime

class CreateReactionPostEnterpriseDTO(ORJSONModel):
    post_enterprise_id: int = Field(..., ge=1, description="The ID of the post enterprise this post belongs to.")
    reaction_type: ReactionTypeEnum = Field(..., description="The type of reaction being registered.")
