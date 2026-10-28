import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints, field_validator

import app.core.exceptions as e

# Requests

class RegisterUserRequest(BaseModel):
  username: ValidUsername
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
  username: ValidUsername
  email: EmailStr


# Validated Type

ValidUsername = Annotated[
  str,
  StringConstraints(
    min_length=1,
    max_length=30
  )
]