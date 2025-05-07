from abc import ABC
from typing import Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl

from src.models.users import Role, Gender


class UserResponseSchema(BaseModel):
    password: Annotated[str, Field(min_length=6, max_length=255)]
    full_name: Annotated[str, Field(min_length=6, max_length=255)]
    email: EmailStr
    role: Role
    age: int
    gender: Gender


class UserCreationSchema(BaseModel):
    password: Annotated[str, Field(min_length=6, max_length=255)]
    full_name: Annotated[str, Field(min_length=6, max_length=255)]
    email: EmailStr
    age: int
    gender: Gender
    

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserProfileSchema(BaseModel):
    email: EmailStr
    full_name: str
    gender: Gender
    age: int
    photo_count: int

class UpdateUserProfileSchema(BaseModel):
    full_name: str
    email: EmailStr

class UserMeSchema(BaseModel):
    email: EmailStr
    full_name: str
    gender: Gender
    age: int
    created_at: datetime
    updated_at: datetime
