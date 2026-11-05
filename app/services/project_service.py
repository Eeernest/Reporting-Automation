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
    client_id: int,
    name: str,
    location: str | None = None,
    description: str | None = None,
    est_end_date: date | None = None,
    act_end_date: date | None = None
  ) -> Project:
    project_obj = Project(
      client_id=client_id,
      name=name,
      location=location,
      description=description,
      est_end_date=est_end_date,
      act_end_date=act_end_date
    )

    return await self._try_commit_project_obj(project_obj)


  # Helper Methods

  # project_repo and session

  async def _try_commit_project_obj(self, project_obj: Project) -> Project:
    try:
      added_project_obj = await self.project_repo.add_project(project_obj)

      await self.session.commit()

      return added_project_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc