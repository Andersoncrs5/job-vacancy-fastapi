from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel

class CreateUserDTO(ORJSONModel):
    name: str = Field(..., min_length=4, max_length=50, description="The name field should be between 4 and 50")
    email: EmailStr = Field(..., min_length=8, max_length=150, description="The email field should be between 8 and 150")
    bio: str | None = Field(None, max_length=600, description="The bio field should have size max of 50")
    password: str = Field(..., min_length=6, max_length=50, description="The password field should be between 6 and 50")
    avatar_url: str | None = Field(None, max_length=255, description="The avatar url field should have size max of 255")

    def to_user_entity(self):
        from app.configs.db.database import UserEntity
        
        return UserEntity(
            name = self.name,
            email = self.email,
            password = self.password,
            bio = self.bio,
            avatar_url = self.avatar_url,
        )
    
class UpdateUserDTO(ORJSONModel):
    name: str | None = Field(None, max_length=50, description="The name field should have size max of 50")
    password: str | None = Field(None, max_length=50, description="The password field should have size max of 50")
    bio: str | None = Field(None, max_length=600, description="The bio field should have size max of 600")
    avatar_url: str | None = Field(None, max_length=255, description="The avatar url field should have size max of 255")

class LoginDTO(ORJSONModel):
    email: EmailStr = Field(..., min_length=8, max_length=150, description="The email field should be between 8 and 150")
    password: str = Field(..., min_length=6, max_length=50, description="The password field should be between 6 and 50")

class UserOUT(ORJSONModel):
    id: int
    name: str
    email: str
    avatar_url: str | None
    bio: str | None
    created_at: datetime | str
