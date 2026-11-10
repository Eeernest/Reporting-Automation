from fastapi import APIRouter, status

from app.dependencies.item_dependency import ItemServiceDep
from app.dependencies.permit_dependency import CurrentUserDep
import app.schemas.item_schema as s

router = APIRouter()

@router.post(
  "/register_item",
  response_model=s.RegisterItemResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_item(
  current_user: CurrentUserDep,
  service: ItemServiceDep,
  request: s.RegisterItemRequest,
):
  return await service.register_item(
    user_id=current_user.id,
    project_id=request.project_id,
    name=request.name,
    item_type=request.item_type,
    item_status=request.item_status,
    description=request.description
  )