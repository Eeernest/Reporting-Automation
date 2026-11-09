from enum import Enum

class ItemStatus(str, Enum):
  measurements = "Measurements"
  estimation = "Estimation"
  material_ordering = "Material Ordering"
  production = "Production"
  installation = "Installation"
  completed = "Completed"
  cancelled = "Cancelled"

class ItemType(str, Enum):
  bathroom_vanity = "Bathroom Vanity"
  kitchen = "Kitchen"
  other = "Other"
  overhead_cabinets = "Overhead Cabinets"
  tv_unit = "TV Unit"
  wardrobe = "Wardrobe"