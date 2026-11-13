from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService

# Main functions

def get_expense_service(session: SessionDep):
  expense_repo = ExpenseRepository(session)

  return ExpenseService(expense_repo, session)


# Alias Variables

ExpenseServiceDep = Annotated[ExpenseService, Depends(get_expense_service)]