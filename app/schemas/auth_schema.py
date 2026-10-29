from pydantic import BaseModel

import app.core.types as t

# Requests

class LogoutRequest(BaseModel):
  refresh_token: t.ValidJWTToken

class RefreshRequest(BaseModel):
  refresh_token: t.ValidJWTToken


# Responses

class LoginResponse(BaseModel):
  access_token: t.ValidJWTToken
  refresh_token: t.ValidJWTToken
  token_type: t.ValidJWTTokenType

class RefreshResponse(BaseModel):
  access_token: t.ValidJWTToken
  refresh_token: t.ValidJWTToken
  token_type: t.ValidJWTTokenType