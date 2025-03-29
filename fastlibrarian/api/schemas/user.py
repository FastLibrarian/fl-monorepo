"""User schema models."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class User(UserBase):
    """Schema for user responses."""

    id: int
    is_active: bool = True

    class Config:
        """Pydantic config."""

        from_attributes = True


from .book import Book

User.model_rebuild()
