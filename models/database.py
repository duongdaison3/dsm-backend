from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy chuỗi kết nối DB (sẽ tạo ở bước sau)
DATABASE_URL = os.getenv("DATABASE_URL")

# Khởi tạo engine (echo=True giúp in ra các câu lệnh SQL trên terminal để dễ debug)
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Import các model vào đây để SQLModel nhận diện được trước khi tạo bảng
    from .user import User
    from .daily_note import DailyNote
    from .weekly_report import WeeklyReport
    
    SQLModel.metadata.create_all(engine)