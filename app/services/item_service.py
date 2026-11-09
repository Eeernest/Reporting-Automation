from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.enums.item_enum import ItemStatus, ItemType
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.repositories.project_repository import ProjectRepository

class ItemService:
  def __init__(
    self,
    item_repo: ItemRepository,
    project_repo: ProjectRepository,
    session: AsyncSession
  ):
    self.item_repo = item_repo
    self.project_repo = project_repo
    self.session = session

  # Main Methods

  async def register_item(
    self,
    user_id: int,
    project_id: int,
    name: str,
    item_type: ItemType,
    item_status: ItemStatus,
    description: str | None = None
  ) -> Item:
    await self._check_project_obj_existance(project_id, user_id)

    item_obj = Item(
      project_id=project_id,
      name=name,
      item_type=item_type,
      item_status=item_status,
      description=description
    )

    return await self._try_commit_item_obj(item_obj)


  # Helper Methods

  # item_repo and session

  async def _try_commit_item_obj(self, item_obj: Item) -> Item:
    try:
      added_item_obj = await self.item_repo.add_item(item_obj)

      await self.session.commit()

      return added_item_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc


  # project_repo

  async def _check_project_obj_existance(self, project_id: int, user_id: int) -> None:
    project_obj = await self.project_repo.get_by_id_and_user_id(project_id, user_id)

    if not project_obj:
      raise e.ProjectNotFoundError()