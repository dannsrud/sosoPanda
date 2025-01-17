# CUDA 지원 PyTorch 기본 이미지 사용
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 포트 설정
EXPOSE 8501

# 실행 명령어
CMD ["streamlit", "run", "src/web/app.py", "--server.address", "0.0.0.0"]
