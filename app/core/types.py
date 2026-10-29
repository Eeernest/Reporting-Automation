from typing import Annotated

from pydantic import StringConstraints

# User Model related types

ValidUsername = Annotated[str, StringConstraints(min_length=1, max_length=30)]