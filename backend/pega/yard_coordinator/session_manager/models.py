from enum import Enum

from pydantic import BaseModel
from typing import List, Optional, Dict

from backend.modules.models import Task


class Hostler(BaseModel):
    checker_id: str
    name: str
    moves: int
    tasks: List[Task] = []


class PollResult(BaseModel):
    workbasket_tasks: List[Task]
    hostlers: Dict[str, Hostler]


class ReCreateHostler(BaseModel):
    checker_id: Optional[str]
    hostler_name: Optional[str]
    password: str = "123456"


class LoginError(Exception):
    """Raised when login fails."""
    pass
