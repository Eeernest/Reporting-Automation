from typing import TypedDict

class AccessTokenPayload(TypedDict):
  iss: str
  sub: str
  role: str
  aud: str
  iat: int
  exp: int
  jti: str

class RefreshTokenPayload(TypedDict):
  iss: str
  sub: str
  aud: str
  iat: int
  exp: int
  jti: str