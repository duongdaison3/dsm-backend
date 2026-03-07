from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date, datetime
import uuid

class DailyNote(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True) # Ràng buộc khóa ngoại với bảng User
    note_date: date = Field(default_factory=date.today, index=True)
    highlight: str
    follow_up: str
    blockers: str
    one_percent_better: Optional[str] = None
    meeting_notes: Optional[str] = None
    planned_tasks: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)