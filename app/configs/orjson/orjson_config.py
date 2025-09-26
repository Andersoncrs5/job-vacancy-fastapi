import orjson
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

def orjson_default(obj):
    if isinstance(obj, UUID):
        return obj.hex 
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        from_attributes = True
