from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.dependencies.project_dependency import VerifiedProjectDep
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.services.item_service import ItemService

# Main Functions

def get_item_service(session: SessionDep):
  item_repo = ItemRepository(session)

  return ItemService(item_repo, session)

async def get_verified_item(
  item_id: int,
  verified_project: VerifiedProjectDep,
  service: ItemServiceDep
) -> Item:
  return await service.get_item(item_id, verified_project.id)


# Alias Variables

ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]

VerifiedItemDep = Annotated[Item, Depends(get_verified_item)]