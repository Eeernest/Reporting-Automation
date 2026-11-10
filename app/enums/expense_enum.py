from enum import Enum

class ExpenseType(str, Enum):
  hardware = "Hardware"
  logistics = "Logistics"
  materials = "Materials"
  other = "Other"
  subcontractors = "Subcontractors"
  tooling = "Tooling"