# 🚀 TOTAL DSM WebApp - Backend API

Đây là hệ thống Backend cung cấp API cho nền tảng **Daily Standup Meeting (DSM)**, được thiết kế để quản lý tiến độ công việc hàng ngày của nhân sự và tự động hóa việc tổng hợp báo cáo bằng AI.

## 🛠️ Công nghệ sử dụng

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - Framework Python siêu tốc độ.
- **Database:** PostgreSQL (lưu trữ đám mây trên [Neon.tech](https://neon.tech/)).
- **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/) (kết hợp sức mạnh của SQLAlchemy & Pydantic).
- **AI Integration:** Google Gemini AI (`google-generativeai`).
- **Security:** JSON Web Tokens (JWT) & bcrypt (Mã hóa mật khẩu).
- **Deployment:** [Render](https://render.com/).

## ✨ Tính năng cốt lõi

1. **Xác thực & Phân quyền:** Đăng nhập an toàn với JWT, phân chia Role rõ ràng (Admin, Depart, Staff).
2. **Quản lý Nhật ký (Daily Notes):** API CRUD cho phép nhân sự nộp highlight, blockers và kế hoạch 1% Better mỗi ngày.
3. **Tích hợp AI (Gemini):** Tự động đọc dữ liệu nhật ký trong tuần và generate ra báo cáo tổng hợp thông minh cho quản lý.
4. **Thống kê Admin:** API tính toán tỷ lệ chuyên cần và chất lượng bài viết theo thời gian thực.

## 🚀 Hướng dẫn cài đặt môi trường Local

**1. Clone kho lưu trữ này về máy:**

````bash
git clone [https://github.com/duongdaison3/dsm-backend.git](https://github.com/duongdaison3/dsm-backend.git)
cd dsm-backend

**2. Tạo môi trường ảo và cài đặt thư viện:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

**3. Tạo file .env ở thư mục gốc và cấu hình:**
```bash
DATABASE_URL=postgresql://<user>:<password>@<host>/<db_name>?sslmode=require
SECRET_KEY=your_secret_key
ALGORITHM=HS256
GEMINI_API_KEYS=your_gemini_key_1,your_gemini_key_2

**4. Khởi chạy Server:**
```bash
uvicorn main:app --reload
API Docs (Swagger UI) sẽ có sẵn tại: http://localhost:8000/docs

👨‍💻 Tác giả: Pea Dương - Sinh viên năm cuối Khoa CNTT @ Đại học Phenikaa.
````
