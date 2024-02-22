from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from .tags import TagResponse
from .auth import UserResponse

class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: List[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    tags: List[TagResponse]
    tags: List[UserResponse]

    class Config:
        orm_mode = True





