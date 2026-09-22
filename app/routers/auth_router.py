from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth_dependency import AuthServiceDep
from app.schemas.token_schema import TokenLogoutRequest, TokenResponse

router = APIRouter()

@router.post(
  "/login",
  response_model=TokenResponse,
  status_code=status.HTTP_200_OK
)
async def login(
  service: AuthServiceDep,
  login_data: OAuth2PasswordRequestForm = Depends()
):
  return await service.login(login_data.username, login_data.password)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(service: AuthServiceDep, logout_request: TokenLogoutRequest):
  await service.logout(logout_request)

  return status.HTTP_204_NO_CONTENT