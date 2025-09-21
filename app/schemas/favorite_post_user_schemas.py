from pydantic import BaseModel
from app.schemas.post_user_schemas import PostUserOUT
from app.schemas.user_schemas import UserOUT
from datetime import datetime

class FavoritePostUserOUT(BaseModel):
    id: int
    owner: UserOUT
    post: PostUserOUT
    created_at: datetime | str

    class Config:
        from_attributes = True