from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber

# Requests

class RegisterClientRequest(BaseModel):
  name: ValidName
  phone_number: PolishNumber
  email: EmailStr | None = None
  notes: ValidNotes | None = None
  

# Responses

class RegisterClinetResponse(BaseModel):
  id: int
  user_id: int
  name: ValidName
  phone_number: PolishNumber
  email: EmailStr | None = None


# Validated Typer

ValidName = Annotated[
  str,
  StringConstraints(
    min_length=1,
    max_length=32
  )
]

class PolishNumber(PhoneNumber):
  default_region_code = "PL"
  supported_regions = ["PL"]
  phone_format = "E164"

ValidNotes = Annotated[
  str,
  StringConstraints(
    min_length=1,
    max_length=300
  )
]