import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_if_missing")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

def get_password_hash(password: str) -> str:
    # bcrypt yêu cầu dữ liệu đầu vào phải là dạng bytes
    pwd_bytes = password.encode('utf-8')
    # Tạo chuỗi muối (salt) ngẫu nhiên
    salt = bcrypt.gensalt()
    # Băm mật khẩu
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Trả về chuỗi string để lưu vào database
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # So sánh mật khẩu gốc và mật khẩu đã băm
    return bcrypt.checkpw(password_byte_enc, hashed_password_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt