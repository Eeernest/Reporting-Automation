from enum import Enum

class UserRole(str, Enum):
  user = "ROLE_USER"
  admin = "ROLE_ADMIN"