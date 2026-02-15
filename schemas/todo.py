import uuid
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 2

# Input Schemas

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    priority: Priority = Priority.LOW

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool | None = None
    priority: Priority | None = None

class TodoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID 
    title: str
    description: str | None
    is_completed: bool
    priority: int 
    created_at: datetime
    updated_at: datetime
    owner_id: uuid.UUID

