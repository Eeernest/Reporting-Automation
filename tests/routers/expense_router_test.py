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


# register_expense_for_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_expense_for_item(
  integ_expense_router,
  registered_project_obj,
  registered_item_obj
):
  request = {
    "expense_type": "Hardware",
    "amount": 3000.23
  }

  result = await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}/expenses",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"]
  assert data["project_id"]
  assert data["item_id"]
  assert data["expense_type"]
  assert data["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_expense_for_item_credentials_validation_error(
  integ_expense_router,
  registered_project_obj,
  registered_item_obj
):
  request = {
    "expense_type": "wrong_expense",
    "amount": 0.001
  }

  result = await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}/expenses",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "expense_type"
  assert data["detail"][1]["field_name"] == "amount"


# update_expense_for_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_expense_for_project(
  integ_expense_router,
  registered_expense_obj,
  registered_project_obj
):
  request = {"amount": 123321.32}

  result = await integ_expense_router.patch(
    f"/projects/{registered_project_obj.id}/expenses/{registered_expense_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["project_id"]
  assert data["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_udpate_expense_for_project_invalid_credentials_validation_error(
  integ_expense_router,
  registered_expense_obj,
  registered_project_obj
):
  request = {
    "expense_type": "wrong_expense",
    "amount": 0.001
  }

  result = await integ_expense_router.patch(
    f"/projects/{registered_project_obj.id}/expenses/{registered_expense_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "expense_type"
  assert data["detail"][1]["field_name"] == "amount"

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_expense_for_project_no_field_provided_error(
  integ_expense_router,
  registered_expense_obj,
  registered_project_obj
):
  request = {}

  result = await integ_expense_router.patch(
    f"/projects/{registered_project_obj.id}/expenses/{registered_expense_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_400_BAD_REQUEST
  assert data["detail"] == e.NoFieldProvidedError.detail


# get_expesne_for_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_expense_for_project_success(
  integ_expense_router,
  registered_expense_obj,
):
  result = await integ_expense_router.get(
    f"/projects/{registered_expense_obj.project_id}/expenses/{registered_expense_obj.id}"
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["project_id"]
  assert data["item_id"]
  assert data["expense_type"]
  assert data["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_expense_for_project_not_found_error(integ_expense_router):
  result = await integ_expense_router.get(f"/projects/{123}/expenses/{3213}")

  data = result.json()

  assert result.status_code == status.HTTP_404_NOT_FOUND
  assert data["detail"] == e.ExpenseNotFoundError.detail


# get_expesne_for_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_expense_for_item_success(
  integ_expense_router,
  registered_expense_obj,
):
  expense = registered_expense_obj
  
  result = await integ_expense_router.get(
    f"/projects/{expense.project_id}/items/{expense.item_id}/expenses/{expense.id}"
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["project_id"]
  assert data["item_id"]
  assert data["expense_type"]
  assert data["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_expense_for_item_not_found_error(integ_expense_router):
  result = await integ_expense_router.get(f"/projects/{423}/items/{1}/expenses/{123}")

  data = result.json()

  assert result.status_code == status.HTTP_404_NOT_FOUND
  assert data["detail"] == e.ExpenseNotFoundError.detail


# get_all_expenses_for_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_expenses_for_project_success(
  integ_expense_router,
  registered_project_obj
):
  request = {
    "expense_type": "Logistics",
    "amount": 2585.23
  }

  await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/expenses",
    json=request
  )
  
  result = await integ_expense_router.get(
    f"/projects/{registered_project_obj.id}/expenses"
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert len(data) == 1
  assert data[0]["id"]
  assert data[0]["project_id"]
  assert data[0]["item_id"] is None
  assert data[0]["expense_type"]
  assert data[0]["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_expenses_for_project_return_empty_list_success(
  integ_expense_router
):
  result = await integ_expense_router.get(f"/projects/{12345}/expenses")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert len(data) == 0
  assert data == []


# get_all_expenses_for_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_expenses_for_item_success(
  integ_expense_router,
  registered_project_obj,
  registered_item_obj
):
  request = {
    "expense_type": "Hardware",
    "amount": 3000.23
  }

  await integ_expense_router.post(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}/expenses",
    json=request
  )

  result = await integ_expense_router.get(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}/expenses"
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert len(data) == 1
  assert data[0]["id"]
  assert data[0]["project_id"]
  assert data[0]["item_id"]
  assert data[0]["expense_type"]
  assert data[0]["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_expenses_for_item_return_empty_list_success(integ_expense_router):
  result = await integ_expense_router.get(f"/projects/{13213}/items/{42341}/expenses")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert len(data) == 0
  assert data == []