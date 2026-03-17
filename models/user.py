from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date
from enum import Enum
import uuid

class RoleEnum(str, Enum):
    admin = "admin"
    depart = "depart"
    staff = "staff"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True) # Đã đổi thành username
    hashed_password: str
    full_name: str
    role: str
    is_first_login: bool = True
    avatar_url: Optional[str] = None
    dob: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)