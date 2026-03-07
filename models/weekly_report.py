from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date, datetime
import uuid

class WeeklyReport(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    week_start_date: date = Field(index=True)
    ai_summary: str
    is_edited: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)