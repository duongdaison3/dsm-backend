from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date, datetime

class DailyNote(SQLModel, table=True):
    # Đổi UUID thành int ở 2 dòng này
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id") 
    
    note_date: date
    highlight: str
    follow_up: str
    blockers: str
    one_percent_better: Optional[str] = None
    meeting_notes: Optional[str] = None
    planned_tasks: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)