from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.repositories.client_repository import ClientRepository
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

# Main Functions

def get_project_service(session: SessionDep):
  client_repo = ClientRepository(session)
  project_repo = ProjectRepository(session)

  return ProjectService(client_repo, project_repo, session)


# Alias Variables

ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]