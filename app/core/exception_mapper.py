import app.core.exceptions as e

# Main Functions

def refine_integrity_error(err_msg: str, exc: Exception) -> None:
  constraint_map = {
    "email": e.EmailUnavailableError,
    "username": e.UsernameUnavailableError,
    "user_client_email": e.EmailUnavailableError,
    "user_client_name": e.NameUnavailableError,
    "user_client_phone_number": e.PhoneUnavailableError
  }

  for partial_msg, exc_class in constraint_map.items():
    if partial_msg in err_msg:
      raise exc_class() from exc

  raise e.DatabaseIntegrityError() from exc