from datetime import date
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository

class ProjectService:
  def __init__(self, project_repo: ProjectRepository, session: AsyncSession):
    self.project_repo = project_repo
    self.session = session

  # Main Mehods

  async def register_project(
    self,
    user_id: int,
    client_id: int,
    name: str,
    location: str | None = None,
    description: str | None = None,
    est_end_date: date | None = None,
    act_end_date: date | None = None
  ) -> Project:
    project_obj = Project(
      user_id=user_id,
      client_id=client_id,
      name=name,
      location=location,
      description=description,
      est_end_date=est_end_date,
      act_end_date=act_end_date
    )

    added_project_obj = await self._add_project_or_raise(project_obj)

    await self._commit_project_or_raise(added_project_obj)

    return added_project_obj

  async def update_project(
    self,
    project_obj: Project,
    update_data: dict[str, Any]
  ) -> Project:
    updated_project_obj = self._update_project_or_raise(project_obj, update_data)

    await self._commit_project_or_raise(updated_project_obj)

    return updated_project_obj

  async def get_project(self, project_id: int, user_id: int, client_id: int) -> Project:
    return await self._get_project_or_raise(project_id, user_id, client_id)

  async def get_all_projects(self, user_id: int, client_id: int) -> list[Project]:
    return await self.project_repo.get_all_by_owner(user_id, client_id)


  # Helper Methods

  # project_repo

  async def _add_project_or_raise(self, project_obj: Project) -> Project:
    try:
      return await self.project_repo.add_project(project_obj)

    except IntegrityError as exc:
      raise e.DatabaseIntegrityError() from exc

  async def _get_project_or_raise(
    self,
    project_id: int,
    user_id: int,
    client_id: int
  ) -> Project:
    project_obj = await self.project_repo.get_by_id_and_owner(
      project_id,
      user_id,
      client_id
    )

    if not project_obj:
      raise e.ProjectNotFoundError()

    return project_obj


  # session

  async def _commit_project_or_raise(self, project_obj: Project) -> None:
    try:
      await self.session.commit()
      await self.session.refresh(project_obj)

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc


  # Object

  def _update_project_or_raise(
    self,
    project_obj: Project,
    update_data: dict[str, Any]
  ) -> Project:
    if not update_data:
      raise e.NoFieldProvidedError()
    
    for field, value in update_data.items():
      setattr(project_obj, field, value)

    return project_obj