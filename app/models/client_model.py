from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base

class Client(Base):
  __tablename__ = "clients"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False, unique=True, index=True)
  company = Column(String, unique=True)
  email = Column(String, unique=True)
  phone_number = Column(Integer, nullable=False, unique=True)
  created_at = Column(DateTime, default=datetime.now(timezone.utc))
  updated_at = Column(
    DateTime,
    default=datetime.now(timezone.utc),
    onupdate=datetime.now(timezone.utc)
  )