import orjson
from pydantic import BaseModel

class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()
        from_attributes = True
