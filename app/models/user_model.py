from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, nullable=False, unique=True, index=True)
  email = Column(String, nullable=False, unique=True, index=True)
  hashed_password = Column(String, nullable=False)
  user_role = Column(String, index=True)
  is_active = Column(Boolean, default=True)
  is_deleted = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)