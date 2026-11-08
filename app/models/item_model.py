from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Relationship

from app.db.database import Base

# Enums

class ItemStatus(str, Enum):
  measurements = "Measurements"
  estimation = "Estimation"
  material_ordering = "Material Ordering"
  production = "Production"
  installation = "Installation"
  completed = "Completed"
  cancelled = "Cancelled"

class ItemType(str, Enum):
  bathroom_vanity = "Bathroom Vanity"
  kitchen = "Kitchen"
  other = "Other"
  overhead_cabinets = "Overhead Cabinets"
  tv_unit = "TV Unit"
  wardrobe = "Wardrobe"


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

  project = Relationship("Project", back_populates="project_item")