# backend/main.py (Cập nhật)
from fastapi import FastAPI
from models.database import create_db_and_tables
from routers import users, auth, notes, report # Import router mới
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DSM WebApp API",
    description="API cho hệ thống Daily Standup Meeting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cho phép mọi nguồn gốc (origin)
    allow_credentials=True,
    allow_methods=["*"], # Cho phép mọi phương thức (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Cho phép mọi header
)

app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Tích hợp Router users vào ứng dụng chính
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(report.router)
@app.get("/")
def read_root():
    return {"message": "Server DSM WebApp đang hoạt động ngon lành!"}