from fastapi import APIRouter, status

from app.dependencies.permit_dependency import CurrentUserDep
from app.dependencies.project_dependency import ProjectServiceDep
import app.schemas.project_schema as s

router = APIRouter()

@router.post(
  "/register_project",
  response_model=s.RegisterProjectResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_project(
  current_user: CurrentUserDep,
  service: ProjectServiceDep,
  request: s.RegisterProjectRequest
):
  return await service.register_project(
    user_id=current_user.id,
    client_id=request.client_id,
    name=request.name,
    location=request.location,
    description=request.description,
    est_end_date=request.est_end_date,
    act_end_date=request.act_end_date
  )