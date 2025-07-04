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
