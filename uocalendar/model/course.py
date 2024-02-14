from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Course:
  class_name: str = None
  class_code: str = None
  class_data: list = field(default_factory=list)