from fastapi import APIRouter, status

from app.dependencies.item_dependency import ItemServiceDep, VerifiedItemDep
from app.dependencies.project_dependency import VerifiedProjectDep
import app.schemas.item_schema as s

router = APIRouter()

@router.post(
  "/projects/{project_id}/items",
  response_model=s.RegisterItemResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_item(
  verified_project: VerifiedProjectDep,
  service: ItemServiceDep,
  request: s.RegisterItemRequest,
):
  return await service.register_item(
    project_id=verified_project.id,
    name=request.name,
    item_type=request.item_type,
    item_status=request.item_status,
    description=request.description
  )

@router.patch(
  "/projects/{project_id}/items/{item_id}",
  response_model=s.UpdateItemResponse,
  status_code=status.HTTP_200_OK
)
async def update_item(
  item: VerifiedItemDep,
  service: ItemServiceDep,
  request: s.UpdateItemRequest
):
  return await service.update_item(
    item_obj=item,
    update_data=request.model_dump(exclude_unset=True)
  )

@router.delete(
    "/projects/{project_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_item(item: VerifiedItemDep, service: ItemServiceDep):
  return await service.delete_item(item_obj=item)

@router.get(
  "/projects/{project_id}/items/{item_id}",
  response_model=s.GetItemResponse,
  status_code=status.HTTP_200_OK
)
async def get_item(
  item_id: int,
  project: VerifiedProjectDep,
  service: ItemServiceDep
):
  return await service.get_item(
    item_id=item_id,
    project_id=project.id,
    user_id=project.user_id
  )

@router.get(
  "/projects/{project_id}/items",
  response_model=list[s.GetItemResponse],
  status_code=status.HTTP_200_OK
)
async def get_all_items(project: VerifiedProjectDep, service: ItemServiceDep):
  return await service.get_all_items(project_id=project.id, user_id=project.user_id)