from unittest.mock import AsyncMock, Mock

import pytest
from redis.asyncio import Redis
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.db.database import Base
from app.models.user_model import User

pytest_plugins = [
  "anyio",
  "tests.fixtures.token_fixture",
  "tests.fixtures.user_fixture",
]

@pytest.fixture(scope="session")
def anyio_backend():
  return "asyncio"

@pytest.fixture(scope="session")
async def redis_container():
  with RedisContainer("redis:7") as rdc:
    host = rdc.get_container_host_ip()
    port = rdc.get_exposed_port(6379)

    client = Redis(
      host=host,
      port=port,
      decode_responses=True
    )

    yield client

    await client.flushall()
    await client.aclose()

@pytest.fixture(scope="session")
def postgres_container():
  with PostgresContainer("postgres:16-alpine") as postgres:
    yield postgres

@pytest.fixture(scope="session")
def test_engine(postgres_container):
  url = postgres_container.get_connection_url().replace("postgresql+psycopg2", "postgresql+asyncpg")

  engine = create_async_engine(
    url,
    poolclass=NullPool,
  )

  return engine

@pytest.fixture(scope="session")
async def setup_database(test_engine):
  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  yield 

  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
  
  await test_engine.dispose()

@pytest.fixture
async def db_session(test_engine, setup_database):
  conn = await test_engine.connect()
  trans = await conn.begin()

  test_async_session = async_sessionmaker(
    bind=conn,
    class_=AsyncSession,
    expire_on_commit=False,
    join_transaction_mode="create_savepoint"
  )

  async with test_async_session() as session:
    try:
      yield session
    finally:
      await session.close()
      await trans.rollback()
      await conn.close()


# Dependency Mocks

@pytest.fixture()
def mock_security():
  mock = AsyncMock()
  mock.create_access_token_payload = Mock()
  mock.create_refresh_token_payload = Mock()
  mock.encode_jwt_token = Mock()

  return mock

@pytest.fixture()
def mock_user_repo():
  return AsyncMock()

@pytest.fixture()
def mock_token_repo():
  return AsyncMock()