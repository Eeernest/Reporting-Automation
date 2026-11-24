from fastapi import APIRouter, status

from app.dependencies.expense_dependency import ExpenseServiceDep, VerifiedProjectExpenseDep, VerifiedItemExpenseDep
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

@router.patch(
  "/projects/{project_id}/expenses/{expense_id}",
  response_model=s.UpdateExpenseResponse,
  status_code=status.HTTP_200_OK
)
async def update_expesnse_for_project(
  expense: VerifiedProjectExpenseDep,
  request: s.UpdateExpenseRequest,
  service: ExpenseServiceDep
):
  return await service.update_expense(
    expense_obj=expense,
    update_data=request.model_dump(exclude_unset=True)
  )

@router.patch(
  "/projects/{project_id}/items/{item_id}/expenses/{expense_id}",
  response_model=s.UpdateExpenseResponse,
  status_code=status.HTTP_200_OK
)
async def update_expense_for_item(
  expense: VerifiedItemExpenseDep,
  request: s.UpdateExpenseRequest,
  service: ExpenseServiceDep 
):
  return await service.update_expense(
    expense_obj=expense,
    update_data=request.model_dump(exclude_unset=True),
  )

@router.delete(
  "/projects/{project_id}/expenses/{expense_id}",
  status_code=status.HTTP_204_NO_CONTENT
)
async def delete_expense_for_project(
  expense: VerifiedProjectExpenseDep,
  service: ExpenseServiceDep
):
  return await service.delete_expense(expense)

@router.delete(
  "/projects/{project_id}/items/{item_id}/expenses/{expense_id}",
  status_code=status.HTTP_204_NO_CONTENT
)
async def delete_expense_for_item(
  expense: VerifiedItemExpenseDep,
  service: ExpenseServiceDep
):
  return await service.delete_expense(expense)

@router.get(
  "/projects/{project_id}/expenses/{expense_id}",
  response_model=s.GetExpenseResponse,
  status_code=status.HTTP_200_OK
)
async def get_expense_for_project(
  expense_id: int,
  project: VerifiedProjectDep,
  service: ExpenseServiceDep
):
  return await service.get_expense(
    expense_id=expense_id,
    project_id=project.id,
  )

@router.get(
  "/projects/{project_id}/items/{item_id}/expenses/{expense_id}",
  response_model=s.GetExpenseResponse,
  status_code=status.HTTP_200_OK
)
async def get_expense_for_item(
  expense_id: int,
  item: VerifiedItemDep,
  service: ExpenseServiceDep
):
  return await service.get_expense(
    expense_id=expense_id,
    project_id=item.project_id,
    item_id=item.id
  )

@router.get(
  "/projects/{project_id}/expenses",
  response_model=list[s.GetExpenseResponse],
  status_code=status.HTTP_200_OK
)
async def get_all_expenses_for_project(
  project: VerifiedProjectDep,
  service: ExpenseServiceDep
):
  return await service.get_all_expenses(project_id=project.id)

@router.get(
  "/projects/{project_id}/items/{item_id}/expenses",
  response_model=list[s.GetExpenseResponse],
  status_code=status.HTTP_200_OK
)
async def get_all_expenses_for_item(item: VerifiedItemDep, service: ExpenseServiceDep):
  return await service.get_all_expenses(
    project_id=item.project_id,
    item_id=item.id
  )