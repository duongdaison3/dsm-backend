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
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: RoleEnum = Field(default=RoleEnum.staff)
    is_first_login: bool = Field(default=True)
    avatar_url: Optional[str] = None
    dob: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)