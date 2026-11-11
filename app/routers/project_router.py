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
  current_user: CurrentUserDep,
  client: VerifiedClientDep,
  service: ProjectServiceDep,
  request: s.RegisterProjectRequest
):
  return await service.register_project(
    user_id=current_user.id,
    client_id=client.id,
    name=request.name,
    location=request.location,
    description=request.description,
    est_end_date=request.est_end_date,
    act_end_date=request.act_end_date
  )