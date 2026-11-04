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