from fastapi import APIRouter, status

from app.dependencies.user_dependency import UserServiceDep
from app.schemas.user_schema import UserCreateRequest, UserResponse

router = APIRouter()

@router.post(
  "/register_user",
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED,
)
async def register_user(service: UserServiceDep, user_request_data: UserCreateRequest):
  return await service.create_account(user_request_data)