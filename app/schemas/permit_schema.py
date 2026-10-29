from pydantic import BaseModel, EmailStr

import app.core.types as t

# Responses

class GetCurrentUserResponse(BaseModel):
  id: int
  username: t.ValidUsername
  email: EmailStr