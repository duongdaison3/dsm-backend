# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models.database import engine
from models.user import User
from utils.security import verify_password, create_access_token

router = APIRouter(tags=["Authentication"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Bước 1: Tìm user trong database bằng email (OAuth2 mặc định dùng trường 'username', nên ta map nó với email)
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    # Bước 2: Kiểm tra sự tồn tại của user và độ chính xác của mật khẩu
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Bước 3: Đăng nhập thành công, tạo Token nhét thông tin (email, role, is_first_login) vào
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "is_first_login": user.is_first_login}
    )
    
    # Bước 4: Trả token về cho Frontend
    return {"access_token": access_token, "token_type": "bearer"}