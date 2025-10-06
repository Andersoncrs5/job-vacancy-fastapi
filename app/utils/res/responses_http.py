from app.utils.res.response_body import ResponseBody
from typing import Final, Dict, Any

RESPONSE_401: Final[Dict] = {
    "description": "Token invalid",
    "model": ResponseBody
}

RESPONSE_409: Final[Dict] = {
    "description": "COnflict of datas",
    "model": ResponseBody
}

RESPONSE_403: Final[Dict] = {
    "description": "Forbbin of make such action",
    "model": ResponseBody
}

RESPONSE_400: Final[Dict] = {
    "description": "",
    "model": ResponseBody
}

RESPONSE_400_ID_REQUIRED: Final[Dict] = {
    "description": "Id is required",
    "model": ResponseBody
}

RESPONSE_404: Final[Dict] = {
    "description": "Entity not found",
    "model": ResponseBody
}

RESPONSE_404_USER: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody
}

RESPONSE_404_INDUSTRY: Final[Dict] = {
    "description": "Industry not found",
    "model": ResponseBody
}

RESPONSE_404_POST_USER: Final[Dict] = {
    "description": "Post User not found",
    "model": ResponseBody
}

RESPONSE_404_CATEGORY: Final[Dict] = {
    "description": "Category not found",
    "model": ResponseBody
}

RESPONSE_404_POST: Final[Dict] = {
    "description": "Post not found",
    "model": ResponseBody
}

RESPONSE_500: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody[Any]
}