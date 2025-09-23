from fastapi.testclient import TestClient
from typing import Final
from app.schemas.media_post_user_schemas import *
from tests.integration.helper import create_and_login_user, create_enterprise, create_post_user, create_category, create_favorite_post_user
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/media-post-user'