from fastapi import APIRouter, status

from app.dependencies.client_dependency import ClientServiceDep
from app.dependencies.permit_dependency import CurrentUserDep
import app.schemas.client_schema as s

router = APIRouter()

@router.post(
  "/clients",
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

@router.get(
  "/clients/{client_id}",
  response_model=s.GetClientResponse,
  status_code=status.HTTP_200_OK
)
async def get_client(
  current_user: CurrentUserDep,
  client_id: int,
  service: ClientServiceDep
):
  return await service.get_client(client_id, current_user.id)