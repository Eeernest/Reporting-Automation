from pydantic import BaseModel

import app.core.types as t
from app.enums.expense_enum import ExpenseType

# Requests

class RegisterExpenseRequest(BaseModel):
  expense_type: ExpenseType
  amount: t.ValidMoney | None = None


# Responses

class RegisterExpenseResponse(BaseModel):
  id: int
  project_id: int
  item_id: int | None
  expense_type: ExpenseType
  amount: t.ValidMoney | None

class GetExpenseResponse(BaseModel):
  id: int
  project_id: int
  item_id: int | None
  expense_type: ExpenseType
  amount: t.ValidMoney | None