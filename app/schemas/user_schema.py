import re

from pydantic import BaseModel, EmailStr, field_validator

import app.core.exceptions as e
import app.core.types as t

# Requests

class RegisterUserRequest(BaseModel):
  username: t.ValidUsername
  email: EmailStr
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

class RegisterUserResponse(BaseModel):
  id: int
  username: t.ValidUsername
  email: EmailStr