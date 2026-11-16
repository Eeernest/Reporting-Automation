from fastapi import status
import pytest

import app.core.exceptions as e

# register_expense

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_expense_for_project_success(
  integ_expense_router,
  registered_project_obj,
):
  request = {
    "expense_type": "Logistics",
    "amount": 2585.23
  }

  result = await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/expenses",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"]
  assert data["project_id"]
  assert data["item_id"] is None
  assert data["expense_type"]
  assert data["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_expense_for_project_credentials_validation_error(
  integ_expense_router,
  registered_project_obj,
  registered_item_obj
):
  request = {
    "expense_type": "Invalid Expense",
    "amount": -1234.1231
  }

  result = await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/expenses",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "expense_type"
  assert data["detail"][1]["field_name"] == "amount"