from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# ── User schemas ─────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def username_rules(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be 50 characters or fewer")
        if not v.isalnum():
            raise ValueError("Username may only contain letters and numbers")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Post schemas ──────────────────────────────────────────────────────────────

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

    @field_validator("title")
    @classmethod
    def title_rules(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(v) > 200:
            raise ValueError("Title must be 200 characters or fewer")
        return v

    @field_validator("content")
    @classmethod
    def content_rules(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Content must be at least 10 characters")
        if len(v) > 10_000:
            raise ValueError("Content must be 10 000 characters or fewer")
        return v


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}