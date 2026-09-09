from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError

from app.core.exceptions import AppError
from app.core.exception_handler import custom_exc_handler, validation_exc_handler
from app.routers.user_router import router as user_router

app = FastAPI()

app.add_exception_handler(AppError, custom_exc_handler)
app.add_exception_handler(RequestValidationError, validation_exc_handler)

app.include_router(user_router)