from pydantic import BaseModel

import app.core.types as t
from app.enums.item_enum import ItemStatus, ItemType

# Requests

class RegisterItemRequest(BaseModel):
  user_id: int
  project_id: int
  name: t.ValidItemName
  item_type: ItemType
  item_status: ItemStatus
  description: t.ValidItemDescription | None = None


# Responses

class RegisterItemResponse(BaseModel):
  id: int
  project_id: int
  name: t.ValidItemName
