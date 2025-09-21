from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user, create_category
from main import app
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

URL: Final[str] = "/api/v1/post-user"

