from enum import Enum

class UserRole(Enum, str):
  user = "ROLE_USER"
  admin = "ROLE_ADMIN"