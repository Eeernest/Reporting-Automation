from jwt.exceptions import PyJWTError, ExpiredSignatureError
import pytest
from redis.exceptions import RedisError

import app.core.exceptions as e

# login method

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_success(
  mock_security,
  mock_user_repo,
  mock_token_repo,
  unit_auth_service,
  token_response_obj,
  token_dict,
  mock_user_obj
):
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True
  mock_security.create_access_token_payload.return_value = token_dict
  mock_security.create_refresh_token_payload.return_value = token_dict
  mock_token_repo.store_refresh_token.return_value = None
  mock_security.encode_jwt_token.side_effect = [
    token_response_obj.access_token,
    token_response_obj.refresh_token
  ]

  result = await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert result.access_token == token_response_obj.access_token
  assert result.refresh_token == token_response_obj.refresh_token
  assert result.token_type == token_response_obj.token_type

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_not_found(mock_security, mock_user_repo, unit_auth_service):
  mock_user_repo.get_by_username.return_value = None
  mock_security.verify_password.return_value = False

  with pytest.raises(e.InvalidCredentialsError) as exc:
    await unit_auth_service.login("username", "Password123")

  assert exc.value.status_code == e.InvalidCredentialsError.status_code
  assert exc.value.detail == e.InvalidCredentialsError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_wrong_password(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = False

  with pytest.raises(e.InvalidCredentialsError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.InvalidCredentialsError.status_code
  assert exc.value.detail == e.InvalidCredentialsError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_is_inactive(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_obj.is_active = False
  
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True

  with pytest.raises(e.UserInactiveError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.UserInactiveError.status_code
  assert exc.value.detail == e.UserInactiveError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_deleted(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_obj.is_deleted = True  

  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True


  with pytest.raises(e.UserDeletedError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.UserDeletedError.status_code
  assert exc.value.detail == e.UserDeletedError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_redis_failure_error(
  mock_security,
  mock_token_repo,
  mock_user_repo,
  unit_auth_service,
  token_dict,
  mock_user_obj
):
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_paassword.return_value = True
  mock_security.create_access_token_payload.return_value = token_dict
  mock_security.create_refresh_token_payload.return_value = token_dict
  mock_token_repo.store_refresh_token.side_effect = RedisError

  with pytest.raises(e.RedisFailureError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.RedisFailureError.status_code
  assert exc.value.detail == e.RedisFailureError.detail


# logout

@pytest.mark.anyio
@pytest.mark.unit
async def test_logout_success(
  mock_security,
  mock_token_repo,
  unit_auth_service,
  token_logout_obj,
  token_dict
):
  mock_security.decode_jwt_token.return_value = token_dict
  mock_token_repo.delete_refresh_token.return_value = None

  result = await unit_auth_service.logout(token_logout_obj)

  assert result == None

@pytest.mark.anyio
@pytest.mark.unit
async def test_logout_pyjwterror(mock_security, unit_auth_service, token_logout_obj):
  mock_security.decode_jwt_token.side_effect = PyJWTError

  result = await unit_auth_service.logout(token_logout_obj)

  assert result == None


# restore_tokens

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_success(
  mock_security,
  mock_token_repo,
  mock_user_repo,
  unit_auth_service,
  token_restore_obj,
  token_response_obj,
  token_dict,
  mock_user_obj
):
  mock_security.decode_jwt_token.return_value = token_dict
  mock_token_repo.delete_refresh_token.return_value = None
  mock_user_repo.get_by_id.return_value = mock_user_obj
  mock_security.create_access_token_payload.return_value = token_dict
  mock_security.create_refresh_token_payload.return_value = token_dict
  mock_token_repo.store_refresh_token.return_value = None
  mock_security.encode_jwt_token.side_effect = [
    token_response_obj.access_token,
    token_response_obj.refresh_token
  ]

  result = await unit_auth_service.restore_tokens(token_restore_obj)

  assert result.access_token == token_response_obj.access_token
  assert result.refresh_token == token_response_obj.refresh_token
  assert result.token_type == token_response_obj.token_type

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_expired_signature_error(
  mock_security,
  unit_auth_service,
  token_restore_obj
):
  mock_security.decode_jwt_token.side_effect = ExpiredSignatureError()

  with pytest.raises(e.TokenExpiredError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.TokenExpiredError.status_code
  assert exc.value.detail == e.TokenExpiredError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_pyjwterror(
  mock_security,
  unit_auth_service,
  token_restore_obj
):
  mock_security.decode_jwt_token.side_effect = PyJWTError()

  with pytest.raises(e.InvalidCredentialsError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.InvalidCredentialsError.status_code
  assert exc.value.detail == e.InvalidCredentialsError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_false_refresh_token(
  mock_security,
  unit_auth_service,
  token_restore_obj,
  token_dict
):
  token_dict["refresh"] = False
  
  mock_security.decode_jwt_token.return_value = token_dict

  with pytest.raises(e.InvalidTokenError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_redis_delete_failure(
  mock_security,
  mock_token_repo,
  unit_auth_service,
  token_restore_obj,
  token_dict
):
  mock_security.decode_jwt_token.return_value = token_dict
  mock_token_repo.delete_refresh_token.side_effect = RedisError

  with pytest.raises(e.RedisFailureError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.RedisFailureError.status_code
  assert exc.value.detail == e.RedisFailureError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_user_not_found(
  mock_security,
  mock_token_repo,
  mock_user_repo,
  unit_auth_service,
  token_restore_obj,
  token_dict
):
  mock_security.decode_jwt_token.return_value = token_dict
  mock_token_repo.delete_refresh_token.return_value = None
  mock_user_repo.get_by_id.return_value = None

  with pytest.raises(e.InvalidTokenError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_restore_tokens_redis_store_error(
  mock_security,
  mock_token_repo,
  mock_user_repo,
  unit_auth_service,
  token_restore_obj,
  token_dict,
  mock_user_obj 
):
  mock_security.decode_jwt_token.return_value = token_dict
  mock_token_repo.delete_refresh_token.return_value = None
  mock_user_repo.get_by_id.return_value = mock_user_obj
  mock_security.create_access_token_payload.return_value = token_dict
  mock_security.create_refresh_token_payload.return_value = token_dict
  mock_token_repo.store_refresh_token.side_effect = RedisError

  with pytest.raises(e.RedisFailureError) as exc:
    await unit_auth_service.restore_tokens(token_restore_obj)

  assert exc.value.status_code == e.RedisFailureError.status_code
  assert exc.value.detail == e.RedisFailureError.detail