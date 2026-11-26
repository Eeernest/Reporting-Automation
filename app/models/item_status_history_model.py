from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from app.db.database import Base

# Models

class ItemStatusHistory(Base):
  __tablename__ = "item_status_history"

  id = Column(Integer, primary_key=True, index=True)
  item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
  item_status = Column(String, nullable=False, index=True)
  execution_date = Column(Date, nullable=False, default=date.today(), index=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


  # Relationship

  item = Relationship("Item", back_populates="item_status_history")