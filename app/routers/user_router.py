from fastapi import APIRouter, status

from app.dependencies.user_dependency import UserServiceDep
from app.schemas.user_schema import RegisterRequest, RegisterResponse

router = APIRouter()

@router.post(
  "/register",
  response_model=RegisterResponse,
  status_code=status.HTTP_201_CREATED
)
async def register(service: UserServiceDep, register_request: RegisterRequest):
  return await service.create_account(
    username=register_request.username,
    email=register_request.email,
    password=register_request.password
  )