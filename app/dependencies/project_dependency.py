from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.dependencies.permit_dependency import CurrentUserDep
from app.models.project_model import Project
from app.repositories.client_repository import ClientRepository
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

# Main Functions

def get_project_service(session: SessionDep):
  client_repo = ClientRepository(session)
  project_repo = ProjectRepository(session)

  return ProjectService(client_repo, project_repo, session)

async def get_verified_project(
  project_id: int,
  current_user: CurrentUserDep,
  service: ProjectServiceDep
) -> Project:
  return await service.get_project(project_id, current_user.id)


# Alias Variables

ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]

VerifiedProjectDep = Annotated[Project, Depends(get_verified_project)]