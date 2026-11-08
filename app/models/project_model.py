from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import Relationship

from app.db.database import Base

class Project(Base):
  __tablename__ = "projects"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
  client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
  name = Column(String, nullable=False)
  location = Column(String)
  description = Column(String)
  est_end_date = Column(Date)
  act_end_date = Column(Date)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


  # Relationships

  client = Relationship("Client", back_populates="client_projects")
  user = Relationship("User", back_populates="user_project")