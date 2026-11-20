from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.enums.expense_enum import ExpenseType
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository

class ExpenseService:
  def __init__(self, expense_repo: ExpenseRepository, session: AsyncSession):
    self.expense_repo = expense_repo
    self.session = session

  # Main Methods

  async def register_expense(
    self,
    project_id: int,
    expense_type: ExpenseType,
    item_id: int | None = None,
    amount: Decimal | None = None    
  ) -> Expense:
    expense_obj = Expense(
      project_id=project_id,
      item_id=item_id,
      expense_type=expense_type,
      amount=amount
    )

    return await self._commit_expense_or_raise(expense_obj)

  async def get_expense(
    self,
    expense_id: int,
    project_id: int,
    item_id: int | None = None
  ) -> Expense:
    return await self._get_expense_or_raise(expense_id, project_id, item_id)

  async def get_all_expenses(
    self,
    project_id: int,
    item_id: int | None = None
  ) -> list[Expense]:
    return await self.expense_repo.get_all_by_owner(project_id, item_id)


  # Helper Methods

  # expense_repo

  async def _get_expense_or_raise(
    self,
    expense_id: int,
    project_id: int,
    item_id: int | None = None
  ) -> Expense:
    expense_obj = await self.expense_repo.get_by_id_and_owner(
      expense_id,
      project_id,
      item_id
    )

    if not expense_obj:
      raise e.ExpenseNotFoundError()

    return expense_obj


  # expense_repo and session

  async def _commit_expense_or_raise(self, expense_obj: Expense) -> Expense:
    try:
      added_expense_obj = await self.expense_repo.add_expense(expense_obj)

      await self.session.commit()

      return added_expense_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc