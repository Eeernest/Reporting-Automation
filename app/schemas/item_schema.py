from pydantic import BaseModel

import app.core.types as t

# Requests

class RegisterItemRequest(BaseModel):
  user_id: int
  project_id: int
  name: t.ValidItemName
  description: t.ValidItemDescription | None = None


# Responses

class RegisterItemResponse(BaseModel):
  id: int
  project_id: int
  name: t.ValidItemName
