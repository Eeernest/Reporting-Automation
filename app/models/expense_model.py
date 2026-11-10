from datetime import datetime

from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Relationship

from app.db.database import Base

class Expense(Base):
  __tablename__ = "expenses"

  id = Column(Integer, primary_key=True, index=True)
  project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
  item_id = Column(Integer, ForeignKey("items.id"), index=True)
  expense_type = Column(String, nullable=False, index=True)
  amount = Column(Float)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


  # Relationships

  item = Relationship("Item", back_populates="item_expense")
  project = Relationship("Project", back_populates="project_expense")