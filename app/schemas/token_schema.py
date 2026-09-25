from pydantic import BaseModel

class TokenBase(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str


# Requests

class TokenLogoutRequest(BaseModel):
  refresh_token: str

class TokenRestoreRequest(BaseModel):
  refresh_token: str


# Responses

class TokenResponse(TokenBase):
  pass