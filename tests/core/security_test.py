import pytest

import app.core.exceptions as e

# get_password_hash and verify_password

@pytest.mark.anyio
@pytest.mark.unit
async def test_password_hashing_happy_path(unit_security):
  hashed_password = await unit_security.get_password_hash("Password123")

  result = await unit_security.verify_password("Password123", hashed_password)

  assert result is True

@pytest.mark.anyio
@pytest.mark.unit
async def test_password_hashing_wrong_password(unit_security):
  hashed_password = await unit_security.get_password_hash("Password123")
  
  result = await unit_security.verify_password("WrongPassword", hashed_password)
  
  assert result is False


# create_access_token_payload

@pytest.mark.unit
def test_create_access_token_payload_succss(unit_security, mock_user_obj):
  result = unit_security.create_access_token_payload(
    mock_user_obj.id,
    mock_user_obj.user_role
  )

  assert result["sub"] == str(mock_user_obj.id)
  assert result["role"] == mock_user_obj.user_role
  assert result["jti"] is not None


# create_refresh_token_payload

@pytest.mark.unit
def test_create_refresh_token_payload_success(unit_security):
  result = unit_security.create_refresh_token_payload("1")

  assert result["sub"] == "1"
  assert result["jti"] is not None


# get_encoded_access_token

@pytest.mark.unit
def test_get_encoded_access_token_success(unit_security, access_payload_obj):
  result = unit_security.get_encoded_access_token(access_payload_obj)

  assert result is not None


# get_encoded_refresh_token

@pytest.mark.unit
def test_get_encoded_refresh_token_success(unit_security, refresh_payload_obj):
  result = unit_security.get_encoded_access_token(refresh_payload_obj)

  assert result is not None


# get_decoded_access_token

@pytest.mark.unit
def test_get_decoded_access_token_success(unit_security, access_payload_obj):
  encoded_acc_token = unit_security.get_encoded_access_token(access_payload_obj)
  
  result = unit_security.get_decoded_access_token(encoded_acc_token)

  assert result == access_payload_obj


@pytest.mark.unit
def test_get_decoded_access_token_invalid_token_error(unit_security):
  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_access_token("invalid_token")

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.unit
def test_get_decoded_access_token_wrong_header_error(
  unit_security,
  refresh_payload_obj
):
  encoded_ref_token = unit_security.get_encoded_refresh_token(refresh_payload_obj)

  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_access_token(encoded_ref_token)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.anyio
def test_get_decoded_access_token_expired_error(
  unit_security,
  expired_access_payload_obj
):
  encoded_acc_token = unit_security.get_encoded_access_token(expired_access_payload_obj)

  with pytest.raises(e.TokenExpiredError) as exc:
    unit_security.get_decoded_access_token(encoded_acc_token)

  assert exc.value.status_code == e.TokenExpiredError.status_code
  assert exc.value.detail == e.TokenExpiredError.detail

@pytest.mark.anyio
def test_get_decoded_access_token_pyjwterror(unit_security, access_payload_obj):
  access_payload_obj["aud"] = "wrong_aud"

  encoded_acc_token = unit_security.get_encoded_access_token(access_payload_obj)
  
  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_access_token(encoded_acc_token)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail


# get_decoded_refresh_token

@pytest.mark.unit
def test_get_decoded_refresh_token_success(unit_security, refresh_payload_obj):
  encoded_ref_token = unit_security.get_encoded_refresh_token(refresh_payload_obj)
  
  result = unit_security.get_decoded_refresh_token(encoded_ref_token)

  assert result == refresh_payload_obj


@pytest.mark.unit
def test_get_decoded_refresh_token_invalid_token_error(unit_security):
  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_refresh_token("invalid_token")

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.unit
def test_get_decoded_refresh_token_wrong_header_error(
  unit_security,
  access_payload_obj
):
  encoded_acc_token = unit_security.get_encoded_access_token(access_payload_obj)

  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_refresh_token(encoded_acc_token)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.anyio
def test_get_decoded_refresh_token_expired_error(
  unit_security,
  expired_refresh_payload_obj
):
  encoded_ref_token = unit_security.get_encoded_refresh_token(expired_refresh_payload_obj)

  with pytest.raises(e.TokenExpiredError) as exc:
    unit_security.get_decoded_refresh_token(encoded_ref_token)

  assert exc.value.status_code == e.TokenExpiredError.status_code
  assert exc.value.detail == e.TokenExpiredError.detail

@pytest.mark.anyio
def test_get_decoded_access_token_pyjwterror(unit_security, refresh_payload_obj):
  refresh_payload_obj["iss"] = "wrong_iss"

  encoded_acc_token = unit_security.get_encoded_refresh_token(refresh_payload_obj)
  
  with pytest.raises(e.InvalidTokenError) as exc:
    unit_security.get_decoded_refresh_token(encoded_acc_token)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail