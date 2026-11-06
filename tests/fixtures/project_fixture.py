from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

# Integration

@pytest.fixture
def integ_project_repo(db_session):
  return ProjectRepository(db_session)


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