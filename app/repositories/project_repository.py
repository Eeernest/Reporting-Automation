from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_model import Project

class ProjectRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def add_project(self, project_obj: Project) -> Project:
    self.session.add(project_obj)
    await self.session.flush()

    return project_obj

  async def get_by_id_and_user_id(self, project_id: int, user_id: int) -> Project | None:
    result = await self.session.execute(
      select(Project).where(Project.id == project_id, Project.user_id == user_id)
    )

    return result.scalar_one_or_none()