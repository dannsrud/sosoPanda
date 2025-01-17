# backend/storage.py

import os
from datetime import datetime

UPLOAD_DIR = "storage/uploads"
CONVERTED_DIR = "storage/converted"

async def save_uploaded_file(file) -> str:
    """
    print("File Object:", file)
    print("File Filename:", file.filename)

    # 파일을 저장할 경로 생성 (예: timestamp_파일명)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_filename = file.filename if file.filename else "unknown_file"
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 없으면 생성
    upload_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{original_filename}")

    # 파일을 지정된 경로에 저장
    try:
        with open(upload_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        print("Error saving file:", e)
        raise e
    print("Saving file to:", upload_path)
    
    return upload_path
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())
    return upload_path

async def save_converted_image(converted_filename: str, upload_path: str) -> str:
    converted_path = os.path.join(CONVERTED_DIR, converted_filename)
    # 변환된 이미지 저장 로직 (이미지 처리 후 반환된 경로)
    # 저장된 경로 반환
    return converted_path

