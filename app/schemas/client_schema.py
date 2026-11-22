from pydantic import BaseModel, EmailStr

import app.core.types as t

# Requests

class RegisterClientRequest(BaseModel):
  name: t.ValidClientName
  phone_number: t.PolishNumber
  email: EmailStr | None = None
  notes: t.ValidClientNotes | None = None

class UpdateClientRequest(BaseModel):
  name: t.ValidClientName | None = None
  email: EmailStr | None = None
  phone_number: t.PolishNumber | None = None
  notes: t.ValidClientNotes | None = None
  

# Responses

class RegisterClinetResponse(BaseModel):
  id: int
  user_id: int
  name: t.ValidClientName
  phone_number: t.PolishNumber
  email: EmailStr | None

class UpdateClientResponse(BaseModel):
  id: int
  user_id: int
  name: t.ValidClientName | None = None
  email: EmailStr | None = None
  phone_number: t.PolishNumber | None = None
  notes: t.ValidClientNotes | None = None  

class GetClientResponse(BaseModel):
  id: int
  user_id: int
  name: t.ValidClientName
  email: EmailStr | None
  phone_number: t.PolishNumber
  notes: t.ValidClientNotes | None