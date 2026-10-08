from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import Relationship

from app.db.database import Base

class Client(Base):
  __tablename__ = "clients"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
  name = Column(String, nullable=False, index=True)
  company = Column(String)
  email = Column(String)
  phone_number = Column(String, nullable=False)
  notes = Column(String)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(
    DateTime,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )

  user = Relationship("User", back_populates="user_clients")


  __table_args__ = (
    UniqueConstraint("user_id", "name", name="user_client_name"),
    UniqueConstraint("user_id", "phone_number", name="user_client_phone_number"),

    Index(
      "user_client_company",
      "user_id",
      "company",
      unique=True,
      postgresql_where=Column("company").is_not(None)
    ),

    Index(
      "user_client_email",
      "user_id",
      "email",
      unique=True,
      postgresql_where=Column("email").is_not(None)
    )
  )