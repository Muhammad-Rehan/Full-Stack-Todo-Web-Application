from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Index

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """
    Task model representing a todo item with title, description, completion status,
    creation date, and user identifier to establish ownership.
    """
    __table_args__ = (
        Index('idx_task_user_id', 'user_id'),
        Index('idx_task_user_created', 'user_id', 'created_at'),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.user_id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskCreate(TaskBase):
    """Schema for creating a new task (user_id will be set by backend)"""
    pass

class TaskRead(TaskBase):
    """Schema for reading task data"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)
