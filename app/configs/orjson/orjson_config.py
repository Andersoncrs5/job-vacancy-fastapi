import orjson
from pydantic import BaseModel
from uuid import UUID

class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()
        from_attributes = True
        json_encoders={
            UUID: lambda v: str(v)  
        }
