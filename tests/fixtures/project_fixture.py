from datetime import date
from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.permit_dependency import get_current_user
from app.dependencies.project_dependency import get_project_service
from app.main import app
from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

# Integration

@pytest.fixture
def integ_project_repo(db_session):
  return ProjectRepository(db_session)

@pytest.fixture
def integ_project_service(integ_client_repo, integ_project_repo, db_session):
  return ProjectService(integ_client_repo, integ_project_repo, db_session)

@pytest.fixture
async def integ_project_router(integ_project_service, saved_user_obj):
  app.dependency_overrides[get_current_user] = lambda: saved_user_obj
  app.dependency_overrides[get_project_service] = lambda: integ_project_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def mock_project_repo():
  return AsyncMock()

@pytest.fixture
def mock_project_session():
  return AsyncMock()

@pytest.fixture
def unit_project_service(mock_client_repo, mock_project_repo, mock_project_session):
  return ProjectService(mock_client_repo, mock_project_repo, mock_project_session)


# Object

@pytest.fixture
def integ_project_obj(registered_client_obj):
  return Project(
    client_id=registered_client_obj.id,
    name="project name",
    location="location 123",
    description="Description",
    est_end_date=date(2026, 1, 11),
    act_end_date=date(2026, 1, 14)
  )

@pytest.fixture
def unit_project_obj():
  return Project(
    id=11,
    client_id=12,
    name="project name",
    location="location 123",
    description="Description",
    est_end_date=date(2026, 1, 11),
    act_end_date=date(2026, 1, 14)
  )