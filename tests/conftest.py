import pytest
from starlette.testclient import TestClient

from main import app

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client 