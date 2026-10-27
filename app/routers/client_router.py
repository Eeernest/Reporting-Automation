from fastapi import APIRouter, status

from app.dependencies.client_dependency import ClientServiceDep
from app.dependencies.permit_dependency import CurrentUserDep
import app.schemas.client_schema as s

router = APIRouter()

@router.post(
  "/register_client",
  response_model=s.RegisterClinetResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_client(
  current_user: CurrentUserDep,
  service: ClientServiceDep,
  request: s.RegisterClientRequest
):
  return await service.register_client(
    user_id=current_user.id,
    name=request.name,
    email=request.email,
    phone_number=request.phone_number,
    notes=request.notes
  )