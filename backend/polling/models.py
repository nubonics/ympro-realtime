from pydantic import BaseModel
from typing import List, Optional, Dict

class Task(BaseModel):
    id: str
    type: str
    door: str
    trailer: str
    case_id: Optional[str] = None
    trailer_number: Optional[str] = None
    door_number: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    locked: Optional[bool] = None
    created_at: Optional[str] = None  # ISO8601 string
    order: Optional[int] = None
    drop_off_zone: Optional[str] = None
    general_note: Optional[str] = None
    type_of_trailer: Optional[str] = None
    drop_location: Optional[str] = None
    hostler_comments: Optional[str] = None
    yardType: Optional[str] = None

class Hostler(BaseModel):
    id: str
    name: str
    checker_id: str
    moves: int
    tasks: List[Task] = []

class PollResult(BaseModel):
    workbasket_tasks: List[Task]
    hostlers: Dict[str, Hostler]