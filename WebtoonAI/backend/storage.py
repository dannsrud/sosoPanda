# backend/storage.py

import os
from datetime import datetime

UPLOAD_DIR = "storage/uploads"
CONVERTED_DIR = "storage/converted"

# ===============================================
# 업로드파일 저장
# ===============================================
async def save_uploaded_file(file) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())
    return upload_path

# ===============================================
# 변환이미지 저장
# ===============================================
async def save_converted_image(converted_filename: str, upload_path: str) -> str:
    converted_path = os.path.join(CONVERTED_DIR, converted_filename)
    # 변환된 이미지 저장 로직 (이미지 처리 후 반환된 경로)
    # 저장된 경로 반환
    return converted_path

