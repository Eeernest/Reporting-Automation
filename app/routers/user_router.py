from fastapi import APIRouter, status

from app.dependencies.user_dependency import UserServiceDep
import app.schemas.user_schema as s

router = APIRouter()

@router.post(
  "/register_user",
  response_model=s.RegisterUserResponse,
  status_code=status.HTTP_201_CREATED
)
async def register_user(
  service: UserServiceDep,
  register_user_request: s.RegisterUserRequest
):
  return await service.register_user(
    username=register_user_request.username,
    email=register_user_request.email,
    password=register_user_request.password
  )