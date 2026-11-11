from datetime import date

from pydantic import BaseModel

import app.core.types as t

# Requests

class RegisterProjectRequest(BaseModel):
  name: t.ValidProjectName
  location: t.ValidProjectLocation | None = None
  description: t.ValidProjectDescription | None = None
  est_end_date: date | None = None
  act_end_date: date | None = None


# Responses

class RegisterProjectResponse(BaseModel):
  id: int
  user_id: int
  client_id: int
  name: t.ValidProjectName

class GetProjectResposne(BaseModel):
  id: int
  user_id: int
  client_id: int
  name: t.ValidProjectName
  description: t.ValidProjectDescription | None
  est_end_date: date | None
  act_end_date: date | None