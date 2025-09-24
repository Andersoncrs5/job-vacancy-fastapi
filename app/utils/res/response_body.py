from pydantic import BaseModel
from typing import TypeVar, Generic
from app.configs.orjson.orjson_config import ORJSONModel

T = TypeVar('T')

class ResponseBody(ORJSONModel, Generic[T]):
    code: int
    message: str
    body: T
    status: bool
    timestamp: str
    path: str | None
    version: int