from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.dependencies.client_dependency import VerifiedClientDep
from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

# Main Functions

def get_project_service(session: SessionDep):
  project_repo = ProjectRepository(session)

  return ProjectService(project_repo, session)

async def get_verified_project(
  project_id: int,
  client: VerifiedClientDep,
  service: ProjectServiceDep
) -> Project:
  return await service.get_project(project_id, client.user_id, client.id)


# Alias Variables

ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]

VerifiedProjectDep = Annotated[Project, Depends(get_verified_project)]