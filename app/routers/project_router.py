from fastapi import APIRouter, status

from app.dependencies.client_dependency import VerifiedClientDep
from app.dependencies.permit_dependency import CurrentUserDep
from app.dependencies.project_dependency import ProjectServiceDep
import app.schemas.project_schema as s

router = APIRouter()

@router.post(
  "/clients/{client_id}/projects",
  response_model=s.RegisterProjectResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_project(
  client: VerifiedClientDep,
  service: ProjectServiceDep,
  request: s.RegisterProjectRequest
):
  return await service.register_project(
    user_id=client.user_id,
    client_id=client.id,
    name=request.name,
    location=request.location,
    description=request.description,
    est_end_date=request.est_end_date,
    act_end_date=request.act_end_date
  )

@router.get(
  "/clients/{client_id}/projects/{project_id}",
  response_model=s.GetProjectResposne,
  status_code=status.HTTP_200_OK
)
async def get_project(
  project_id: int,
  client: VerifiedClientDep,
  service: ProjectServiceDep
):
  return await service.get_project(project_id, client.user_id, client.id)