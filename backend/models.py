from typing import Annotated, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator


class PullTask(BaseModel):
    id: str
    type: Literal["pull"] = "pull"
    door: str
    trailer: str
    zoneType: str
    zoneLocation: str
    note: str
    priority: str = "normal"
    hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class BringTask(BaseModel):
    id: str
    type: Literal["bring"] = "bring"
    door: str
    trailer: str
    zoneType: str
    zoneLocation: str
    note: str
    priority: str = "normal"
    hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class HookTask(BaseModel):
    id: str
    type: Literal["hook"] = "hook"
    leadTrailer: str
    leadDoor: str
    middleTrailer: Optional[str] = None
    middleDoor: Optional[str] = None
    dolly1: Optional[str] = None
    tailTrailer: str
    tailDoor: Optional[str] = None
    dolly2: Optional[str] = None
    note: str
    priority: str = "normal"
    hostler: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


Task = Annotated[
    Union[PullTask, BringTask, HookTask],
    Field(discriminator="type")
]
