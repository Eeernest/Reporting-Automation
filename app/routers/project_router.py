from fastapi import APIRouter, status

from app.dependencies.client_dependency import VerifiedClientDep
from app.dependencies.permit_dependency import CurrentUserDep
from app.dependencies.project_dependency import ProjectServiceDep, VerifiedProjectDep
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

@router.patch(
  "/clients/{client_id}/projects/{project_id}",
  response_model=s.UpdateProjectResponse,
  status_code=status.HTTP_200_OK
)
async def update_project(
  project: VerifiedProjectDep,
  service: ProjectServiceDep,
  request: s.UpdateProjectRequest
):
  return await service.update_project(
    project_obj=project,
    update_data=request.model_dump(exclude_unset=True)
  )

@router.delete(
  "/clients/{client_id}/projects/{project_id}",
  status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(project: VerifiedProjectDep, service: ProjectServiceDep):
  return await service.delete_project(project)

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
  return await service.get_project(
    project_id=project_id,
    user_id=client.user_id,
    client_id=client.id
  )

@router.get(
  "/clients/{client_id}/projects",
  response_model=list[s.GetProjectResposne],
  status_code=status.HTTP_200_OK
)
async def get_all_projects(client: VerifiedClientDep, service: ProjectServiceDep):
  return await service.get_all_projects(user_id=client.user_id, client_id=client.id)