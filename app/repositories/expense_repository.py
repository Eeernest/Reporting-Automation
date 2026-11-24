from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense_model import Expense

class ExpenseRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def add_expense(self, expense_obj: Expense) -> Expense:
    self.session.add(expense_obj)
    await self.session.flush()

    return expense_obj

  async def delete_expense(self, expense_obj: Expense) -> None:
    await self.session.delete(expense_obj)

  async def get_by_id_and_owner(
    self,
    expense_id: int,
    project_id: int,
    item_id: int | None = None
  ) -> Expense | None:
    stmt = (
      select(Expense)
      .where(
        Expense.id == expense_id,
        Expense.project_id == project_id,
      )
    )

    if item_id:
      stmt.where(Expense.item_id == item_id)

    result = await self.session.execute(stmt)

    return result.scalar_one_or_none()

  async def get_all_by_owner(
    self,
    project_id: int,
    item_id: int | None = None
  ) -> list[Expense]:
    stmt = (
      select(Expense)
      .where(
        Expense.project_id == project_id
      )
    )

    if item_id:
      stmt.where(Expense.item_id == item_id)

    result = await self.session.execute(stmt)

    return list(result.scalars().all())