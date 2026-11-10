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