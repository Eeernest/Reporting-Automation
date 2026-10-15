import re

from pydantic import BaseModel, EmailStr, field_validator

import app.core.exceptions as e

# Schemas

class UserBase(BaseModel):
  username: str
  email: EmailStr

  @field_validator("username")
  def valid_username(cls, v: str) -> str:
    v = v.strip()

    if len(v) > 32:
      raise e.UsernameTooLongError()

    return v


# Requests

class RegisterUserRequest(UserBase):
  password: str

  @field_validator("password")
  def valid_password(cls, v: str) -> str:
    if len(v) < 8:
      raise e.PasswordTooShortError()
    
    if not re.search(r"[A-Z]", v):
      raise e.PasswordNoUppercaseError()
    
    if not re.search(r"\d", v):
      raise e.PasswordNumberError()
    
    return v


# Responses

class RegisterUserResponse(UserBase):
  id: int