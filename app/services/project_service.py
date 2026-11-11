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

    return await self._commit_project_or_raise(project_obj)

  async def get_project(self, project_id: int, user_id: int) -> Project:
    return await self._get_project_or_raise(project_id, user_id)


  # Helper Methods

  # project_repo

  async def _get_project_or_raise(self, project_id: int, user_id: int) -> Project:
    project_obj = await self.project_repo.get_by_id_and_user_id(project_id, user_id)

    if not project_obj:
      raise e.ProjectNotFoundError()

    return project_obj


  # project_repo and session

  async def _commit_project_or_raise(self, project_obj: Project) -> Project:
    try:
      added_project_obj = await self.project_repo.add_project(project_obj)

      await self.session.commit()

      return added_project_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc