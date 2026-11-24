from fastapi import status
import pytest

import app.core.exceptions as e

# register_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_item_success(integ_item_router, registered_project_obj):
  request = {
    "name": "test item",
    "item_type": "Wardrobe",
    "item_status": "Measurements",
    "description": "test description"
  }

  result = await integ_item_router.post(
    f"/projects/{registered_project_obj.id}/items",
    json=request
  )
  
  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"]
  assert data["project_id"]
  assert data["name"]


@pytest.mark.anyio
@pytest.mark.integration
async def test_register_item_credentials_validation_error(
  integ_item_router,
  registered_project_obj
):
  request = {
    "name": "a" * 101,
    "item_type": "invalid_item_type",
    "item_status": "invalid_item_status",
    "description": "b" * 301
  }

  result = await integ_item_router.post(
    f"/projects/{registered_project_obj.id}/items",
    json=request
  )
  
  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "name"
  assert data["detail"][1]["field_name"] == "item_type"
  assert data["detail"][2]["field_name"] == "item_status"
  assert data["detail"][3]["field_name"] == "description"


# update_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_item_success(
  integ_item_router,
  registered_item_obj,
  registered_project_obj
):
  request = {"name": "updated_name"}

  result = await integ_item_router.patch(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["project_id"]
  assert data["name"] == request["name"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_item_invalid_credentials_error(
  integ_item_router,
  registered_item_obj,
  registered_project_obj
):
  request = {
    "name": "a" * 101,
    "item_type": "invalid_item_type",
    "item_status": "invalid_item_status",
    "description": "b" * 301
  }

  result = await integ_item_router.patch(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "name"
  assert data["detail"][1]["field_name"] == "item_type"
  assert data["detail"][2]["field_name"] == "item_status"
  assert data["detail"][3]["field_name"] == "description"

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_item_no_field_provided_error(
  integ_item_router,
  registered_item_obj,
  registered_project_obj
):
  request = {}

  result = await integ_item_router.patch(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_400_BAD_REQUEST
  assert data["detail"] == e.NoFieldProvidedError.detail


# delete_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_delete_item_success(
  integ_item_router,
  registered_item_obj,
  registered_project_obj
):
  result = await integ_item_router.delete(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}"
  )

  assert result.status_code == status.HTTP_204_NO_CONTENT


# get_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_item_success(
  integ_item_router,
  registered_item_obj,
  registered_project_obj
):
  result = await integ_item_router.get(
    f"/projects/{registered_project_obj.id}/items/{registered_item_obj.id}"
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"] == registered_item_obj.id
  assert data["project_id"] == registered_item_obj.project_id
  assert data["name"] == registered_item_obj.name
  assert data["item_type"] == registered_item_obj.item_type
  assert data["item_status"] == registered_item_obj.item_status
  assert data["description"] == registered_item_obj.description

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_item_not_found_error(integ_item_router):
  result = await integ_item_router.get(f"/projects/{1234}/items/{4321}")

  data = result.json()

  assert result.status_code == status.HTTP_404_NOT_FOUND
  assert data["detail"] == e.ItemNotFoundError.detail


# get_all_items

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_items_success(integ_item_router, registered_project_obj):
  request = {
  "name": "test item",
  "item_type": "Wardrobe",
  "item_status": "Measurements",
  "description": "test description"
  }

  saved_item = await integ_item_router.post(
    f"/projects/{registered_project_obj.id}/items",
    json=request
  )

  result = await integ_item_router.get(f"/projects/{registered_project_obj.id}/items")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data[0]["id"]
  assert data[0]["project_id"]
  assert data[0]["name"]
  assert data[0]["item_type"]
  assert data[0]["item_status"]
  assert data[0]["description"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_items_return_empty_success(integ_item_router):
  result = await integ_item_router.get(f"/projects/{55}/items")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data == []