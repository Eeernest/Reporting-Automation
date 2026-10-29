from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber

import app.core.types as t

# Requests

class RegisterClientRequest(BaseModel):
  name: t.ValidClientName
  phone_number: t.PolishNumber
  email: EmailStr | None = None
  notes: t.ValidClientNotes | None = None
  

# Responses

class RegisterClinetResponse(BaseModel):
  id: int
  user_id: int
  name: t.ValidClientName
  phone_number: t.PolishNumber
  email: EmailStr | None = None