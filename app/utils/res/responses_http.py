from app.utils.res.response_body import ResponseBody
from typing import Final, Dict, Any

RESPONSE_401: Final[Dict] = {
    "description": "Token invalid",
    "model": ResponseBody[None]
}

RESPONSE_404_USER: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody[None]
}

RESPONSE_404_POST: Final[Dict] = {
    "description": "Post not found",
    "model": ResponseBody[None]
}

RESPONSE_500: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody[Any]
}