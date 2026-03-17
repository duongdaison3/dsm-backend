from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User
from main import get_session
from utils.security import get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str  # Thay email bằng username
    password: str
    full_name: str
    role: str = "staff"

# API thêm 1 user
@router.post("/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username này đã tồn tại!")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, full_name=user.full_name, role=user.role)
    session.add(new_user)
    session.commit()
    return {"message": "Tạo user thành công"}

# API THÊM HÀNG LOẠT (BULK ADD)
@router.post("/bulk")
def create_users_bulk(users: List[UserCreate], session: Session = Depends(get_session)):
    created_count = 0
    for u in users:
        exist = session.exec(select(User).where(User.username == u.username)).first()
        if not exist:
            hashed = get_password_hash(u.password)
            new_user = User(username=u.username, hashed_password=hashed, full_name=u.full_name, role=u.role)
            session.add(new_user)
            created_count += 1
    session.commit()
    return {"message": f"Đã thêm thành công {created_count} nhân sự!"}