# backend/db.py

import sqlite3
from datetime import datetime

# SQLite 데이터베이스 파일 경로
DB_FILE = "db/database.db"

# 테이블 생성 함수
def initialize_database():
    # SQLite 데이터베이스에 연결
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # `conversion_history` 테이블 생성 (존재하지 않을 경우에만 생성)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversion_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 고유 번호 (자동 증가)
        user_id TEXT DEFAULT 'GUEST' ,  -- 사용자 ID (사용자 테이블과 추후 연결)
        model_name TEXT NOT NULL,  -- 변환 모델명 (모델 정보 테이블과 추후 연결)
        created_at TIMESTAMP,  -- 변환 요청 시각
        processed_at TIMESTAMP,  -- 변환 완료 시각
        original_filename TEXT,  -- 원본 파일 이름
        original_extension TEXT,  -- 원본 파일 확장자 (예: jpg, png)
        original_width INTEGER,  -- 원본 이미지 너비
        original_height INTEGER,  -- 원본 이미지 높이
        original_dpi INTEGER,  -- 원본 이미지 해상도 (dpi)
        original_size INTEGER,  -- 원본 파일 크기 (바이트)
        is_landscape TEXT,  -- 가로 사진 여부(Y/N)
        converted_filename TEXT,  -- 변환된 파일 이름
        conversion_result TEXT,  -- 변환 결과 상세 정보 (성공, 실패, 경고 등)
        processing_time REAL,  -- 변환 처리 시간 (초)
        data_date DATETIME DEFAULT CURRENT_TIMESTAMP  -- 데이터의 년월일시 (기본값: 현재 시각)
    );
    """)

    # 연결 닫기
    conn.commit()
    conn.close()
    print("Database initialized: conversion_history table created (if not exists)")


# 데이터 삽입 예제 함수 (선택적)
def insert_conversion_history(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conversion_history (
        user_id, 
        model_name, 
        created_at,
        processed_at, 
        original_filename, 
        original_extension, 
        original_width, 
        original_height, 
        original_dpi, 
        original_size, 
        is_landscape, 
        converted_filename, 
        conversion_result, 
        processing_time
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()