# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from backend.image_processing import process_image
from backend.storage import save_uploaded_file, save_converted_image
from backend.db import initialize_database, insert_conversion_history
import os
import time
import magic
import re
import uuid
from mimetypes import guess_type
from datetime import datetime
from PIL import Image, UnidentifiedImageError

app = FastAPI()

# 서버 시작 시 데이터베이스 초기화
initialize_database()

UPLOAD_DIR = "storage/uploads"
CONVERTED_DIR = "storage/converted"



# 특수문자 제거 함수
def sanitize_filename(filename: str) -> str:
    # 파일명에서 특수문자 제거
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# 고유한 파일명 생성 함수
def generate_unique_filename(filename: str) -> str:
    # UUID를 이용한 고유한 파일명 생성
    unique_name = str(uuid.uuid4()) + "_" + sanitize_filename(filename)
    return unique_name

@app.post("/transform_image/")
async def transform_image(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
        print("transform_image::[file]=>", file.filename)
        print("transform_image::[model_name]=>", model_name)

        created_at = datetime.now()
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400, detail="Uploaded file is empty. Please upload a valid file."
            )

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(CONVERTED_DIR, exist_ok=True)
        print("1")

        upload_filename = generate_unique_filename(file.filename)
        print("2")
        upload_path = os.path.join(UPLOAD_DIR, upload_filename)
        print("3")

        with open(upload_path, "wb") as f:
            f.write(file_content)
        print("4")

        try:
            original_image = Image.open(upload_path)
            original_image.verify()
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400, detail="Uploaded file is not a valid image."
            )
        
        print("5")
        
        original_image = Image.open(upload_path)
        original_width, original_height = original_image.size
        original_dpi = original_image.info.get("dpi", (72, 72))[0]
        original_size = os.path.getsize(upload_path)
        is_landscape = "Y" if original_width > original_height else "N"

        try:
            converted_filename = process_image(upload_path, model_name)
            conversion_result = "Success"
        except ValueError as e:
            print(f"Error in process_image: {e}")
            converted_filename = None
            conversion_result = "Failure"

        processed_at = datetime.now()
        processing_time = (processed_at - created_at).total_seconds()

        if converted_filename:
        #    converted_path = os.path.join(CONVERTED_DIR, converted_filename)
        #    os.rename(converted_filename, converted_path)
        # 변환된 파일의 원래 위치와 대상 경로를 정확히 지정
            source_path = os.path.join(".", converted_filename)  # 현재 작업 디렉토리에서 변환된 파일
            converted_path = os.path.join(CONVERTED_DIR, converted_filename)

            # 경로를 출력하여 디버깅에 도움
            print(f"Source path: {source_path}, Target path: {converted_path}")

            # 파일 이동
            os.rename(source_path, converted_path)


        else:
            converted_path = None

        data = (
            "GUEST",
            model_name,
            created_at,
            processed_at,
            file.filename,
            os.path.splitext(file.filename)[1].replace(".", ""),
            original_width,
            original_height,
            original_dpi,
            original_size,
            is_landscape,
            os.path.basename(converted_path) if converted_path else None,
            conversion_result,
            processing_time
        )

        insert_conversion_history(data)

        if converted_path:
            return {"filename": os.path.basename(converted_path)}
        else:
            return {"error": conversion_result}
    except HTTPException as e:
        print("HTTPException:", e.detail)
        raise e
    except Exception as e:
        print("Unhandled exception:", str(e))
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the image.",
        )


@app.get("/download/{filename}")
async def download_image(filename: str):
    converted_path = os.path.join(CONVERTED_DIR, filename)
    if os.path.exists(converted_path):
        return FileResponse(converted_path)
    return {"error": "File not found"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    print("Received file:", file.filename)
    return {"filename": filename}