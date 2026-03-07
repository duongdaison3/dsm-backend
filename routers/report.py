from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/reports", tags=["AI Reports"])

# Lấy chuỗi keys từ .env và tách thành danh sách (list)
keys_str = os.getenv("GEMINI_API_KEYS", "")
API_KEYS = [k.strip() for k in keys_str.split(",") if k.strip()]

# Biến toàn cục để nhớ xem đang dùng đến key thứ mấy
current_key_index = 0

def get_next_api_key():
    global current_key_index
    if not API_KEYS:
        return None
    # Lấy key hiện tại
    key = API_KEYS[current_key_index]
    # Tăng index lên 1, nếu vượt quá số lượng key thì quay về 0 (Xoay vòng)
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return key

class ReportRequest(BaseModel):
    weekly_notes: str

@router.post("/generate")
async def generate_weekly_report(request: ReportRequest):
    next_key = get_next_api_key()
    if not next_key:
        raise HTTPException(status_code=500, detail="Hệ thống chưa cấu hình GEMINI_API_KEYS.")
    
    try:
        # Cấu hình Gemini với key vừa được cấp
        genai.configure(api_key=next_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Bạn là một trợ lý AI quản lý nhân sự chuyên nghiệp. Dựa vào các ghi chú công việc hàng ngày dưới đây, hãy tổng hợp thành một báo cáo tuần ngắn gọn, trực quan.
        Chia làm 3 phần rõ ràng, sử dụng icon emoji cho sinh động:
        1. Thành tựu nổi bật.
        2. Khó khăn vướng mắc.
        3. 1% Better & Kế hoạch tiếp theo.

        Dữ liệu nhật ký:
        {request.weekly_notes}
        """
        response = model.generate_content(prompt)
        
        # Có thể in ra terminal để dev biết đang dùng key nào (chỉ hiển thị vài ký tự đầu cho bảo mật)
        print(f"Đã xử lý AI thành công bằng Key bắt đầu với: {next_key[:8]}...")
        
        return {"ai_summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi AI: {str(e)}")