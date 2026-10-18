class AppError(Exception):
  detail = "An error occurred"


# Service Unavailable Errors (503)

class ServiceUnavailableError(AppError):
  pass

class RedisFailureError(ServiceUnavailableError):
  detail = "Redis operation failed"


# Server Error (500)

class ServerError(AppError):
  pass

class DatabaseIntegrityError(ServerError):
  detail = "A database integrity error occured"
  

# Validation Errors (422)

class ValidationError(AppError):
  pass

class PasswordNoUppercaseError(ValidationError):
  detail = "Password should have at least one big letter"

class PasswordNumberError(ValidationError):
  detail = "Password should have at least one number"

class PasswordTooShortError(ValidationError):
  detail = "Password should have at least 8 characters"

class UsernameTooLongError(ValidationError):
  detail = "Username should be shorter than 32 characters"


# Conflict Errors (409)

class ConflictError(AppError):
  pass

class EmailUnavailableError(ConflictError):
  detail = "Email is already in use"

class NameUnavailableError(ConflictError):
  detail = "Name is already in use"

class PhoneUnavailableError(ConflictError):
  detail = "Phone number is already in use"

class UsernameUnavailableError(ConflictError):
  detail = "Username is already in use"


# Forbidden Errors (403)

class ForbiddenError(AppError):
  pass

class UserInactiveError(ForbiddenError):
  detail = "User account is inactive"


# Unauthorized Errors (401)

class UnauthorizedError(AppError):
  pass

class InvalidCredentialsError(UnauthorizedError):
  detail = "Incorrect username or password"

class InvalidTokenError(UnauthorizedError):
  detail = "Could not validate credentials"

class TokenExpiredError(UnauthorizedError):
  detail = "Token expired. Log in again"

class UserDeletedError(UnauthorizedError):
  detail = "User account no longer exists"