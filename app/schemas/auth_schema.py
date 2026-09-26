from pydantic import BaseModel

class AuthBase(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str

# Requests

class LogoutRequest(BaseModel):
  refresh_token: str

class RestoreTokensRequest(BaseModel):
  refresh_token: str


# Responses

class LoginResponse(AuthBase):
  pass

class RestoreTokensResponse(AuthBase):
  pass