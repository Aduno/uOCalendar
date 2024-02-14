from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CourseSection:
    component: str = None
    day: str = None
    time: str = None
    location: str = None
    instructor: str = None
    start_date: str = None
    end_date: str = None