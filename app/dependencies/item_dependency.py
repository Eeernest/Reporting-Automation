from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.repositories.item_repository import ItemRepository
from app.repositories.project_repository import ProjectRepository
from app.services.item_service import ItemService

# Main Functions

def get_item_service(session: SessionDep):
  item_repo = ItemRepository(session)
  project_repo = ProjectRepository(session)

  return ItemService(item_repo, project_repo, session)


# Alias Variables

ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]