from dataclasses import dataclass
from dataclasses import dataclass
from typing import Optional

@dataclass
class CourseData:
  class_name: str = None
  class_code: str = None
  class_data: dict = None