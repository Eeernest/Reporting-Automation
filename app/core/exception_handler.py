from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

import app.core.exceptions as e

# Main functions

def custom_exc_handler(request: Request, exc: e.AppError):
  http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

  for exc_class, status_code in HTTP_STATUS_MAP.items():
    if isinstance(exc, exc_class):
      http_status = status_code
      break
  
  headers = {}

  if http_status == status.HTTP_401_UNAUTHORIZED:
    headers["WWW-Authenticate"] = "Bearer"

  return JSONResponse(
    status_code=http_status,
    content={"detail": exc.detail},
    headers=headers
  )

def validation_exc_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    content={
      "detail": "Wrong input data",
      "errors": exc.errors()
    }
  )


# Maps

HTTP_STATUS_MAP = {
  e.ServiceUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
  e.ServerError: status.HTTP_500_INTERNAL_SERVER_ERROR,
  e.ValidationError: status.HTTP_422_UNPROCESSABLE_CONTENT,
  e.ConflictError: status.HTTP_409_CONFLICT,
  e.ForbiddenError: status.HTTP_403_FORBIDDEN,
  e.UnauthorizedError: status.HTTP_401_UNAUTHORIZED
}