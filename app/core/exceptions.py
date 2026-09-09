class AppError(Exception):
  status_code = 500
  detail = "An error occured"


# Validation Errors (422)

class ValidationError(AppError):
  status_code = 422

class PasswordTooShortError(ValidationError):
  detail = "Password should hate at least 8 characters"

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