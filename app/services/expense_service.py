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
    item_id: int | None,
    expense_type: ExpenseType,
    amount: float | None    
  ) -> Expense:
    expense_obj = Expense(
      project_id=project_id,
      item_id=item_id,
      expense_type=expense_type,
      amount=amount
    )

    return await self._commit_expense_or_raise(expense_obj)


  # Helper Methods

  async def _commit_expense_or_raise(self, expense_obj: Expense) -> Expense:
    try:
      added_expense_obj = await self.expense_repo.add_expense(expense_obj)

      await self.session.commit()

      return added_expense_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc