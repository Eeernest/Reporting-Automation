from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.dependencies.item_dependency import VerifiedItemDep
from app.dependencies.project_dependency import VerifiedProjectDep
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService

# Main functions

def get_expense_service(session: SessionDep):
  expense_repo = ExpenseRepository(session)

  return ExpenseService(expense_repo, session)

async def get_verified_project_expense(
  expense_id: int,
  project: VerifiedProjectDep,
  service: ExpenseServiceDep,
) -> Expense:
  return await service.get_expense(
    expense_id=expense_id,
    project_id=project.id,
  )


# Alias Variables

ExpenseServiceDep = Annotated[ExpenseService, Depends(get_expense_service)]

VerifiedProjectExpenseDep = Annotated[Expense, Depends(get_verified_project_expense)]