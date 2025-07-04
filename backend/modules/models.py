from typing import Annotated, Optional, Union, Literal
from pydantic import BaseModel, Field


class PullTask(BaseModel):
    case_id: str
    yard_task_type: Literal["pull"] = "pull"
    trailer: str  # Required
    assigned_to: Optional[str] = None  # Required, but defaults to None
    door: Optional[str] = None
    zoneType: Optional[str] = None
    zoneLocation: Optional[str] = None
    note: Optional[str] = None
    priority: str = "normal"
    # hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class BringTask(BaseModel):
    case_id: str
    yard_task_type: Literal["bring"] = "bring"
    trailer: str  # Required
    assigned_to: Optional[str] = None  # Required, but defaults to None
    door: Optional[str] = None
    zoneType: Optional[str] = None
    zoneLocation: Optional[str] = None
    note: Optional[str] = None
    priority: str = "normal"
    # hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class HookTask(BaseModel):
    case_id: str
    yard_task_type: Literal["hook"] = "hook"
    trailer: str  # Required
    assigned_to: Optional[str] = None  # Required, but defaults to None
    leadTrailer: Optional[str] = None
    leadDoor: Optional[str] = None
    middleTrailer: Optional[str] = None
    middleDoor: Optional[str] = None
    dolly1: Optional[str] = None
    tailTrailer: Optional[str] = None
    tailDoor: Optional[str] = None
    dolly2: Optional[str] = None
    note: Optional[str] = None
    priority: str = "normal"
    # hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


Task = Annotated[
    Union[PullTask, BringTask, HookTask],
    Field(discriminator="yard_task_type")
]


class DeleteTaskRequest(BaseModel):
    case_id: str


class CreateTaskRequest(BaseModel):
    yard_task_type: str
    trailer: str  # Required
    assigned_to: Optional[str] = None
    door: Optional[str] = None
    # hostler: Optional[str] = None
    status: Optional[str] = "PENDING"
    locked: Optional[bool] = False
    general_note: Optional[str] = ""
    priority: Optional[str] = "Normal"


class TransferTaskRequest(BaseModel):
    case_id: str
    assigned_to: Optional[str] = None
