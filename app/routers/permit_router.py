from fastapi import APIRouter, status

from app.dependencies.permit_dependency import PermitServiceDep, TokenDep
import app.schemas.permit_schema as s

router = APIRouter()

@router.get(
  "/users/me",
  response_model=s.GetCurrentUserResponse,
  status_code=status.HTTP_200_OK
)
async def get_current_user(service: PermitServiceDep, access_token: TokenDep):
  return await service.get_current_user(access_token)