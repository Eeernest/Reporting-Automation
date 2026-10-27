# from atexit import register

# from fastapi import status
# import pytest

# import app.core.exceptions as e

# # register_user

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_success(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "Password123"
#   }
  
#   result = await integ_user_router.post("/register_user", json=request)

#   data = result.json()

#   assert result.status_code == status.HTTP_201_CREATED
#   assert data["id"]

#   @pytest.mark.anyio
#   @pytest.mark.integration
#   async def test_register_user_username_too_long_error(integ_user_router):
#     request = {
#       "username": "a" * 33,
#       "email": "user1@example.com",
#       "password": "Password123"
#     }

#     result = await integ_user_router.post("/register_user", json=request)
#     data = result.json()

#     assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
#     assert data["detail"] == e.UsernameUnavailableError.detail

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_pasword_no_uppercase_error(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "password123"
#   }

#   result = await integ_user_router.post("/register_user", json=request)
#   data = result.json()

#   assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
#   assert data["detail"] == e.PasswordNoUppercaseError.detail

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_pasword_no_number_error(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "Password"
#   }

#   result = await integ_user_router.post("/register_user", json=request)
#   data = result.json()

#   assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
#   assert data["detail"] == e.PasswordNumberError.detail

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_pasword_too_short_error(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "A1123"
#   }

#   result = await integ_user_router.post("/register_user", json=request)
#   data = result.json()

#   assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
#   assert data["detail"] == e.PasswordTooShortError.detail

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_username_unavailable_error(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "Password123"
#   }

#   await integ_user_router.post("/register_user", json=request)
  
#   bad_request = {
#     "username": "user1",
#     "email": "user2@example.com",
#     "password": "HashedPassword123"
#   }

#   result = await integ_user_router.post("/register_user", json=bad_request)
#   data = result.json()

#   assert result.status_code == status.HTTP_409_CONFLICT
#   assert data["detail"] == e.UsernameUnavailableError.detail

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_register_user_email_unavailable_error(integ_user_router):
#   request = {
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "Password123"
#   }

#   await integ_user_router.post("/register_user", json=request)
  
#   bad_request = {
#     "username": "user2",
#     "email": "user1@example.com",
#     "password": "HashedPassword123"
#   }

#   result = await integ_user_router.post("/register_user", json=bad_request)
#   data = result.json()

#   assert result.status_code == status.HTTP_409_CONFLICT
#   assert data["detail"] == e.EmailUnavailableError.detail