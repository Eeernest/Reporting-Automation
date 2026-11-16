from fastapi import APIRouter, status

from app.dependencies.expense_dependency import ExpenseServiceDep
from app.dependencies.item_dependency import VerifiedItemDep
from app.dependencies.project_dependency import VerifiedProjectDep
import app.schemas.expense_schema as s

router = APIRouter()

@router.post(
  "/projects/{project_id}/expenses",
  response_model=s.RegisterExpenseResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_expense_for_project(
  project: VerifiedProjectDep,
  request: s.RegisterExpenseRequest,
  service: ExpenseServiceDep,
):
  return await service.register_expense(
    project_id=project.id,
    expense_type=request.expense_type,
    amount=request.amount
  )

@router.post(
  "/projects/{project_id}/items/{item_id}/expenses",
  response_model=s.RegisterExpenseResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_expense_for_item(
  item: VerifiedItemDep,
  request: s.RegisterExpenseRequest,
  service: ExpenseServiceDep
):
  return await service.register_expense(
    project_id=item.project_id,
    item_id=item.id,
    expense_type=request.expense_type,
    amount=request.amount
  )