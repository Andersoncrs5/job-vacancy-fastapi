from datetime import datetime

from pydantic import Field

from app.configs.db.enums import ReactionTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.post_user_schemas import PostUserOUT
from app.schemas.user_schemas import UserOUT

class ReactionPostUserOUT(ORJSONModel):
    id: int
    user_id: int
    post_user_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime

class ReactionPostUserWithRelationshipOUT(ORJSONModel):
    user_id: int
    post_user_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime
    user: UserOUT
    post: PostUserOUT

class CreateReactionPostUserDTO(ORJSONModel):
    post_user_id: int = Field(..., ge=1, description="The ID of the post enterprise this post belongs to.")
    reaction_type: ReactionTypeEnum = Field(..., description="The type of reaction being registered.")