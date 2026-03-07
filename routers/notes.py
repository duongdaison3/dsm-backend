# backend/routers/notes.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from datetime import date, timedelta # Thêm timedelta
from models.user import User, RoleEnum # Thêm RoleEnum
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, timedelta
import jwt
import os

from models.database import engine
from models.daily_note import DailyNote
from models.user import User

router = APIRouter(prefix="/notes", tags=["Daily Notes"])

# Công cụ lấy Token từ Request Header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_if_missing")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_session():
    with Session(engine) as session:
        yield session

# Hàm giải mã Token để lấy User hiện tại
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except Exception:
        raise HTTPException(status_code=401, detail="Token đã hết hạn hoặc không hợp lệ")
    
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Không tìm thấy User")
    return user

# Schema nhận dữ liệu từ Frontend
class NoteCreate(BaseModel):
    highlight: str
    follow_up: str
    blockers: str
    one_percent_better: Optional[str] = None
    meeting_notes: Optional[str] = None # Thêm dòng này
    planned_tasks: Optional[str] = None # Thêm dòng này

@router.post("/")
def create_note(note: NoteCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    today = date.today()
    
    # Chặn nếu hôm nay user đã viết rồi
    existing_note = session.exec(
        select(DailyNote).where(DailyNote.user_id == current_user.id, DailyNote.note_date == today)
    ).first()
    
    if existing_note:
        raise HTTPException(status_code=400, detail="Bạn đã viết nhật ký cho ngày hôm nay rồi!")

    # Tạo bản ghi mới
    new_note = DailyNote(
        user_id=current_user.id,
        note_date=today,
        highlight=note.highlight,
        follow_up=note.follow_up,
        blockers=note.blockers,
        one_percent_better=note.one_percent_better,
        meeting_notes=note.meeting_notes, # Thêm dòng này
        planned_tasks=note.planned_tasks  # Thêm dòng này
    )
    session.add(new_note)
    session.commit()
    return {"message": "Đã lưu nhật ký thành công!"}

@router.get("/streak", response_model=List[date])
def get_streak(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Lấy danh sách các ngày mà user này ĐÃ viết nhật ký
    notes = session.exec(
        select(DailyNote.note_date)
        .where(DailyNote.user_id == current_user.id)
        .order_by(DailyNote.note_date)
    ).all()
    return notes

# Thêm API này vào cuối file backend/routers/notes.py
@router.get("/{note_date}")
def get_note_by_date(note_date: date, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    note = session.exec(
        select(DailyNote)
        .where(DailyNote.user_id == current_user.id, DailyNote.note_date == note_date)
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhật ký cho ngày này")
    
    return note

@router.get("/admin/stats")
def get_admin_stats(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập")

    yesterday = date.today() - timedelta(days=1)
    
    total_employees = session.exec(select(User).where(User.role != RoleEnum.admin)).all()
    total_count = len(total_employees)

    yesterday_notes = session.exec(select(DailyNote).where(DailyNote.note_date == yesterday)).all()
    submitted_count = len(yesterday_notes)

    # Đếm số người viết TÂM HUYẾT (đủ cả 3 phần highlight, follow_up, blockers)
    fully_completed_count = 0
    blockers = []
    
    for note in yesterday_notes:
        if note.highlight and note.highlight.strip() and \
           note.follow_up and note.follow_up.strip() and \
           note.blockers and note.blockers.strip():
            fully_completed_count += 1
            
        if note.blockers and note.blockers.strip() != "":
            blockers.append(note.blockers)

    return {
        "yesterday_str": yesterday.strftime("%d/%m/%Y"),
        "total_employees": total_count,
        "submitted_count": submitted_count,
        "fully_completed_count": fully_completed_count,
        "blockers": blockers
    }

# Thêm API này vào cuối file backend/routers/notes.py
@router.get("/stats/monthly-public")
def get_monthly_total_stats(session: Session = Depends(get_session)):
    today = date.today()
    # Lấy ngày mùng 1 của tháng hiện tại
    first_day_of_month = today.replace(day=1)
    
    # Đếm tổng số note từ đầu tháng đến nay (của toàn bộ công ty)
    notes = session.exec(
        select(DailyNote).where(DailyNote.note_date >= first_day_of_month)
    ).all()
    
    return {"current_month_count": len(notes)}

# Thêm API mới này vào cuối file
@router.get("/my-streak")
def get_my_streak(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # 1. Lấy toàn bộ ngày đã viết nhật ký của user này, xếp từ cũ nhất đến mới nhất
    notes = session.exec(
        select(DailyNote.note_date)
        .where(DailyNote.user_id == current_user.id)
        .order_by(DailyNote.note_date.asc())
    ).all()

    if not notes:
        return {"streak": 0}

    # 2. Lọc ngày trùng lặp (lỡ 1 ngày sửa note 2 lần)
    unique_dates = sorted(list(set(notes)))
    first_date = unique_dates[0]
    today = date.today()

    streak = 0
    current_date = first_date

    # 3. Chạy vòng lặp thời gian từ ngày đầu tiên đến hôm nay để tính điểm
    while current_date <= today:
        if current_date in unique_dates:
            streak += 1 # Viết -> Cộng 1
        else:
            streak = max(0, streak - 1) # Quên -> Trừ 1 (Tối thiểu là 0)
        current_date += timedelta(days=1)

    return {"streak": streak}