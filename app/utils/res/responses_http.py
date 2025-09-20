from app.utils.res.response_body import ResponseBody
from typing import Final, Dict, Any

RESPONSE_401: Final[Dict] = {
    "description": "Token invalid",
    "model": ResponseBody[None]
}

RESPONSE_400: Final[Dict] = {
    "description": "",
    "model": ResponseBody[None]
}

RESPONSE_400_ID_REQUIRED: Final[Dict] = {
    "description": "Id is required",
    "model": ResponseBody[None]
}

RESPONSE_404_USER: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody[None]
}

RESPONSE_404_INDUSTRY: Final[Dict] = {
    "description": "Industry not found",
    "model": ResponseBody[None]
}

RESPONSE_404_POST_USER: Final[Dict] = {
    "description": "Post User not found",
    "model": ResponseBody[None]
}

RESPONSE_404_CATEGORY: Final[Dict] = {
    "description": "Category not found",
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