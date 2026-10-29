from typing import Annotated, Literal

from pydantic import StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber

# Client Model related types

ValidClientName = Annotated[str, StringConstraints(min_length=1, max_length=32)]

ValidClientNotes = Annotated[str, StringConstraints(min_length=1, max_length=300)]


# JWT token related types

ValidJWTToken = Annotated[str, StringConstraints(min_length=1)]

ValidJWTTokenType = Literal["bearer"]


# User Model related types

ValidUsername = Annotated[str, StringConstraints(min_length=1, max_length=30)]


# Classes

class PolishNumber(PhoneNumber):
  default_region_code = "PL"
  supported_regions = ["PL"]
  phone_format = "E164"