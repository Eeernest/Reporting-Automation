from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.enums.expense_enum import ExpenseType
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.project_repository import ProjectRepository

class ExpenseService:
  def __init__(
    self,
    expense_repo: ExpenseRepository,
    item_repo: ItemRepository,
    project_repo: ProjectRepository,
    session: AsyncSession
  ):
    self.expense_repo = expense_repo
    self.item_repo = item_repo
    self.project_repo = project_repo
    self.session = session

  # Main Methods

  async def register_expense(
    self,
    user_id: int,
    project_id: int,
    item_id: int | None,
    expense_type: ExpenseType,
    amount: float | None
  ) -> Expense:
    await self._check_project_obj_existance(project_id, user_id)

    if item_id:
      await self._check_item_obj_existance(item_id, project_id)

    expense_obj = Expense(
      project_id=project_id,
      item_id=item_id,
      expense_type=expense_type,
      amount=amount
    )

    return await self._try_commit_expense_obj(expense_obj)


  # Helper Methods

  # expense_repo and session

  async def _try_commit_expense_obj(self, expense_obj: Expense) -> Expense:
    try:
      added_expense_obj = await self.expense_repo.add_expense(expense_obj)

      await self.session.commit()

      return added_expense_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc


  # item_repo

  async def _check_item_obj_existance(self, item_id: int, project_id: int) -> None:
    item_obj = await self.item_repo.get_by_id_and_project_id(item_id, project_id)

    if not item_obj:
      raise e.ItemNotFoundError()


  # project_repo

  async def _check_project_obj_existance(self, project_id: int, user_id: int) -> None:
    project_obj = await self.project_repo.get_by_id_and_user_id(project_id, user_id)

    if not project_obj:
      raise e.ProjectNotFoundError()