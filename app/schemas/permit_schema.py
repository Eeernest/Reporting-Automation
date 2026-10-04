from pydantic import BaseModel, EmailStr

# Responses

class GetCurrentUserResponse(BaseModel):
  id: int
  username: str
  email: EmailStr