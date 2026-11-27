from fastapi import APIRouter, status

from app.dependencies.item_dependency import ItemServiceDep, VerifiedItemDep, VerifiedStatusHistoryDep
from app.dependencies.project_dependency import VerifiedProjectDep
import app.schemas.item_schema as s

router = APIRouter()

# Item Model

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
    description=request.description,
    execution_date=request.execution_date
  )

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

@router.patch(
  "/projects/{project_id}/items/{item_id}/status_history",
  response_model=s.ChangeItemStatusResponse,
  status_code=status.HTTP_200_OK
)
async def change_item_status(
  item: VerifiedItemDep,
  service: ItemServiceDep,
  request: s.ChangeItemStatusRequest
):
  return await service.change_item_status(
    item_obj=item,
    item_status=request.item_status,
    execution_date=request.execution_date
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


# ItemStatusHistory Model

@router.get(
  "/projects/{project_id}/items/{item_id}/status_history/{status_history_id}",
  response_model=s.GetStatusHistoryResponse,
  status_code=status.HTTP_200_OK
)
async def get_status_history(
  status_history_id: int,
  item: VerifiedItemDep,
  service: ItemServiceDep
):
  return await service.get_status_history(
    status_history_id=status_history_id,
    item_id=item.id
  )

@router.get(
  "/projects/{project_id}/items/{item_id}/status_history",
  response_model=list[s.GetStatusHistoryResponse],
  status_code=status.HTTP_200_OK
)
async def get_all_status_histories(item: VerifiedItemDep, service: ItemServiceDep):
  return await service.get_all_status_histories(item_id=item.id)

@router.patch(
  "/projects/{project_id}/items/{item_id}/status_history/{status_history_id}",
  response_model=s.UpdateStatusHistoryResponse,
  status_code=status.HTTP_200_OK
)
async def update_status_history(
  status_history: VerifiedStatusHistoryDep,
  service: ItemServiceDep,
  request: s.UpdateStatusHistoryRequest
):
  return await service.update_status_history(
    status_history_obj=status_history,
    update_data=request.model_dump(exclude_unset=True)
  )