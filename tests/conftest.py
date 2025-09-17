import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.configs.db.database import Base, get_db
from main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_engine():
    
    DATABASE_URL = "postgresql+asyncpg://postgres:@localhost:5432/job_vacancy_fast_test"
    engine = create_async_engine(DATABASE_URL)
    yield engine

@pytest.fixture(scope="session")
async def async_session_maker(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture(scope="function", autouse=True)
async def setup_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def async_session(async_session_maker, setup_db):
    async with async_session_maker() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
def test_client(async_session):
    def override_get_db():
        yield async_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()