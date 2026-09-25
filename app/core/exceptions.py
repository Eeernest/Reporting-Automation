class AppError(Exception):
  status_code = 500
  detail = "An error occurred"


# Service Unavailable Errors (503)

class ServiceUnavailableError(AppError):
  status_code = 503

class RedisFailureError(ServiceUnavailableError):
  detail = "Redis operation failed"


# Validation Errors (422)

class ValidationError(AppError):
  status_code = 422

class EmailTooLongError(ValidationError):
  detail = "Email should be shorter than 320 characters"

class UsernameTooLongError(ValidationError):
  detail = "Username should be shorter than 32 characters"

class PasswordTooShortError(ValidationError):
  detail = "Password should have at least 8 characters"

class PasswordNoUppercaseError(ValidationError):
  detail = "Password should have at least one big letter"

class PasswordNumberError(ValidationError):
  detail = "Password should have at least one number"


# Conflict Errors (409)

class ConflictError(AppError):
  status_code = 409

class UsernameUnavailableError(ConflictError):
  detail = "Username is already in use"

class EmailUnavailableError(ConflictError):
  detail = "Email is already in use"


# Forbidden Errors (403)

class ForbiddenError(AppError):
  status_code = 403

class UserInactiveError(ForbiddenError):
  detail = "User account is inactive"


# Unauthorized Errors (401)

class UnauthorizedError(AppError):
  status_code = 401

class InvalidCredentialsError(UnauthorizedError):
  detail = "Incorrect username or password"

class InvalidTokenError(UnauthorizedError):
  detail = "Could not validate credentials"

class TokenExpiredError(UnauthorizedError):
  detail = "Token expired. Log in again"

class UserDeletedError(UnauthorizedError):
  detail = "User account no longer exists"