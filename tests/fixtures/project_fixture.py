from datetime import date

import pytest

from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository

# Integration

@pytest.fixture
def integ_project_repo(db_session):
  return ProjectRepository(db_session)


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