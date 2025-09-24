from pydantic import BaseModel
from app.schemas.post_user_schemas import PostUserOUT
from app.schemas.user_schemas import UserOUT
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel

class FavoritePostUserOUT(ORJSONModel):
    id: int
    owner: UserOUT
    post: PostUserOUT
    created_at: datetime | str