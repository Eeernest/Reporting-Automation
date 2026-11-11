from fastapi import APIRouter, status

from app.dependencies.item_dependency import ItemServiceDep
from app.dependencies.permit_dependency import CurrentUserDep
from app.dependencies.project_dependency import VerifiedProjectDep
import app.schemas.item_schema as s

router = APIRouter()

@router.post(
  "/projects/{project_id}/items",
  response_model=s.RegisterItemResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_item(
  current_user: CurrentUserDep,
  project: VerifiedProjectDep,
  service: ItemServiceDep,
  request: s.RegisterItemRequest,
):
  return await service.register_item(
    user_id=current_user.id,
    project_id=project.id,
    name=request.name,
    item_type=request.item_type,
    item_status=request.item_status,
    description=request.description
  )