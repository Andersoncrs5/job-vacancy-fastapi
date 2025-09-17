from pydantic import BaseModel

class Tokens(BaseModel):
    token: str
    refresh_token: str
    exp_token: str | None
    exp_refresh_token: str | None