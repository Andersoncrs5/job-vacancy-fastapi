from app.configs.orjson.orjson_config import ORJSONModel

class Tokens(ORJSONModel):
    token: str
    refresh_token: str
    exp_token: str | None
    exp_refresh_token: str | None