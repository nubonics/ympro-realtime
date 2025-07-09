from typing import Annotated, Optional, Union, Literal
from pydantic import BaseModel, Field


class PullTask(BaseModel):
    case_id: str
    yard_task_type: Literal["pull"] = "pull"
    trailer: str
    assigned_to: Optional[str] = None
    door: int
    zoneType: Optional[str] = None
    zoneLocation: Optional[str] = None
    note: Optional[str] = None
    priority: str = "normal"
    # --- Grid context fields ---
    row_page: Optional[str] = None
    base_ref: Optional[str] = None
    context_page: Optional[str] = None
    fetch_worklist_pd_key: Optional[str] = None
    team_members_pd_key: Optional[str] = None
    section_id_list: Optional[str] = None
    pzuiactionzzz: Optional[str] = None
    strIndexInList: Optional[str] = None
    activity_params: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class BringTask(BaseModel):
    case_id: str
    yard_task_type: Literal["bring"] = "bring"
    trailer: str
    assigned_to: Optional[str] = None
    door: int
    zoneType: Optional[str] = None
    zoneLocation: Optional[str] = None
    note: Optional[str] = None
    priority: str = "normal"
    # --- Grid context fields ---
    row_page: Optional[str] = None
    base_ref: Optional[str] = None
    context_page: Optional[str] = None
    fetch_worklist_pd_key: Optional[str] = None
    team_members_pd_key: Optional[str] = None
    section_id_list: Optional[str] = None
    pzuiactionzzz: Optional[str] = None
    strIndexInList: Optional[str] = None
    activity_params: Optional[str] = None

    @classmethod
    def check_priority(cls, v):
        if v not in {"low", "normal", "high"}:
            raise ValueError("priority must be low, normal, or high")
        return v


class HookTask(BaseModel):
    case_id: str
    yard_task_type: Literal["hook"] = "hook"
    trailer: str
    assigned_to: Optional[str] = None
    leadTrailer: Optional[str] = None
    leadDoor: Optional[int] = None
    middleTrailer: Optional[str] = None
    middleDoor: Optional[int] = None
    dolly1: Optional[int] = None
    tailTrailer: Optional[str] = None
    tailDoor: Optional[int] = None
    dolly2: Optional[int] = None
    note: Optional[str] = None
    priority: str = "normal"
    # --- Grid context fields ---
    row_page: Optional[str] = None
    base_ref: Optional[str] = None
    context_page: Optional[str] = None
    fetch_worklist_pd_key: Optional[str] = None
    team_members_pd_key: Optional[str] = None
    section_id_list: Optional[str] = None
    pzuiactionzzz: Optional[str] = None
    strIndexInList: Optional[str] = None
    activity_params: Optional[str] = None

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
    priority: Optional[str] = "normal"


# OUTDATED
class TransferTaskRequest(BaseModel):
    case_id: str
    assigned_to: Optional[str] = None


class TransferRequest(BaseModel):
    case_id: str
    assigned_to: str
