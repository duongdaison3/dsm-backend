# backend/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from models.database import engine
from models.user import User, RoleEnum
from utils.security import get_password_hash
import uuid
from typing import Optional
from datetime import date
from routers.notes import get_current_user

# Khởi tạo Router
router = APIRouter(prefix="/users", tags=["Users"])

# Dependency để lấy database session
def get_session():
    with Session(engine) as session:
        yield session

# Schema (Khuôn mẫu) để nhận dữ liệu từ Client (Frontend) gửi lên
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: RoleEnum = RoleEnum.staff

# Schema để trả dữ liệu về (Tuyệt đối KHÔNG trả về hashed_password)
class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: RoleEnum
    is_first_login: bool

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # 1. Kiểm tra xem email đã tồn tại trong DB chưa
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký trong hệ thống!")
    
    # 2. Mã hóa mật khẩu
    hashed_pw = get_password_hash(user.password)
    
    # 3. Tạo bản ghi User mới
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        full_name=user.full_name,
        role=user.role
    )
    
    # 4. Lưu vào Database
    session.add(db_user)
    session.commit()
    session.refresh(db_user) # Lấy lại data mới nhất (bao gồm cả ID vừa được tạo)
    
    return db_user

# Schema nhận dữ liệu update từ Frontend
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    avatar_url: Optional[str] = None

# API Lấy thông tin Profile của chính mình
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# API Cập nhật Profile
@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_update: UserUpdate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.dob is not None:
        current_user.dob = user_update.dob
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
        
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user