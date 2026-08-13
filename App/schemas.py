from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str
    content: str
    favourite: bool = False

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    favourite: Optional[bool] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    favourite: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

