from typing import Annotated, Literal

from pydantic import StringConstraints

# JWT token related types

ValidJWTToken = Annotated[str, StringConstraints(min_length=1)]

ValidJWTTokenType = Literal["bearer"]


# User Model related types

ValidUsername = Annotated[str, StringConstraints(min_length=1, max_length=30)]