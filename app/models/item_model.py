from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Relationship

from app.db.database import Base

# Models

class Item(Base):
  __tablename__ = "items"
  
  id = Column(Integer, primary_key=True, index=True)
  project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
  name = Column(String, nullable=False)
  item_type = Column(String, nullable=False, index=True)
  item_status = Column(String, nullable=False, index=True)
  description = Column(String)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


  # Relationship

  item_expense = Relationship("Expense", back_populates="item", cascade="all, delete-orphan")
  project = Relationship("Project", back_populates="project_item")