from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base

class Client(Base):
  __tablename__ = "clients"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False, index=True)
  company = Column(String)
  email = Column(String)
  phone_number = Column(Integer, nullable=False)
  created_at = Column(DateTime, default=datetime.now(timezone.utc))
  updated_at = Column(
    DateTime,
    default=datetime.now(timezone.utc),
    onupdate=datetime.now(timezone.utc)
  )