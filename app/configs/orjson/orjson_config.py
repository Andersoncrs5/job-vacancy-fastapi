import orjson
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
import json

def orjson_default(obj):
    if isinstance(obj, UUID):
        return str(obj)          

    if isinstance(obj, (date, datetime)):
        return str(obj)

    return json.JSONEncoder().default(obj)

def orjson_dumps(v, *, default=orjson_default):
    return orjson.dumps(v, default=default).decode()

class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        from_attributes = True
