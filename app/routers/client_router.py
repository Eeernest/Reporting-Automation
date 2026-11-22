from fastapi import APIRouter, status

from app.dependencies.client_dependency import ClientServiceDep, VerifiedClientDep
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

@router.patch(
  "/clients/{client_id}",
  response_model=s.UpdateClientResponse,
  status_code=status.HTTP_200_OK
)
async def update_client(
  client: VerifiedClientDep,
  service: ClientServiceDep,
  request: s.UpdateClientRequest
):
  return await service.update_client(
    client_obj=client,
    update_data=request.model_dump(exclude_unset=True)
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

@router.get(
  "/clients",
  response_model=list[s.GetClientResponse],
  status_code=status.HTTP_200_OK
)
async def get_all_clients(current_user: CurrentUserDep, service: ClientServiceDep):
  return await service.get_all_clients(user_id=current_user.id)