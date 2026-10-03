from datetime import datetime, timezone, timedelta

import pytest

from app.core.config import settings
from app.core.security import Security
from app.core.security_types import AccessTokenPayload, RefreshTokenPayload

# Unit

@pytest.fixture()
def unit_security():
  return Security()


# Objects

# Access Token

@pytest.fixture
def access_payload_obj(unit_security, mock_user_obj) -> AccessTokenPayload:
  return unit_security.create_access_token_payload(
    mock_user_obj.id,
    mock_user_obj.user_role
  )

@pytest.fixture
def expired_access_payload_obj(access_payload_obj) -> AccessTokenPayload:
  issued = datetime.now(timezone.utc)
  expired = issued - timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  
  access_payload_obj["exp"] = int(expired.timestamp())

  return access_payload_obj


# Refresh Token

@pytest.fixture
def refresh_payload_obj(unit_security, mock_user_obj) -> RefreshTokenPayload:
  return unit_security.create_refresh_token_payload(mock_user_obj.id)

@pytest.fixture
def expired_refresh_payload_obj(refresh_payload_obj) -> RefreshTokenPayload:
  issued = datetime.now(timezone.utc)
  expired = issued - timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
  
  refresh_payload_obj["exp"] = int(expired.timestamp())

  return refresh_payload_obj