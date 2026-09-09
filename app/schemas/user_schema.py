from enum import Enum
import re

from pydantic import BaseModel, EmailStr, field_validator

import app.core.exceptions as e

# Enums

class UserRole(str, Enum):
  user = "ROLE_USER"
  admin = "ROLE_ADMIN"


# Schemas

class UserBase(BaseModel):
  username: str
  email: EmailStr

  @field_validator("username")
  def valid_username(cls, v: str) -> str:
    v.strip()

    if len(v) > 32:
      raise e.UsernameTooLongError()

    return v

  @field_validator("email")
  def valid_email(cls, v: EmailStr) -> EmailStr:
    v.lower().strip()

    if len(v) > 320:
      raise e.EmailTooLongError()

    return v

class UserCreateRequest(UserBase):
  password: str

  @field_validator("password")
  def valid_password(cls, v: str) -> str:
    if len(v) < 8:
      raise e.PasswordTooShortError()
    
    if not re.search(r"[A-Z]", v):
      raise e.PasswordNoUppercasError()
    
    if not re.search(r"\d", v):
      raise e.PasswordNumberError()
    
    return v

class UserResponse(UserBase):
  id: int