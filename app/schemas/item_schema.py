from datetime import date

from pydantic import BaseModel

import app.core.types as t
from app.enums.item_enum import ItemStatus, ItemType

# Requests

class RegisterItemRequest(BaseModel):
  name: t.ValidItemName
  item_type: ItemType
  item_status: ItemStatus
  description: t.ValidItemDescription | None = None
  execution_date: date | None = None

class UpdateItemRequest(BaseModel):
  name: t.ValidItemName | None = None
  item_type: ItemType | None = None
  description: t.ValidItemDescription | None = None


# Responses

class RegisterItemResponse(BaseModel):
  id: int
  project_id: int
  name: t.ValidItemName

class UpdateItemResponse(BaseModel):
  id: int
  project_id: int
  name: t.ValidItemName | None = None
  item_type: ItemType | None = None
  description: t.ValidItemDescription | None = None

class GetItemResponse(BaseModel):
  id: int
  project_id: int
  name: t.ValidItemName
  item_type: ItemType
  item_status: ItemStatus
  description: t.ValidItemDescription | None