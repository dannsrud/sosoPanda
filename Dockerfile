# 베이스 이미지 설정: Python 3.10의 슬림 버전 사용
FROM python:3.10-slim

# 컨테이너 내 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*  

# Python 패키지 설치를 위한 requirements.txt 파일 복사
COPY requirements.txt .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 전체를 컨테이너로 복사
COPY . .

# Streamlit 서버 설정: 외부 접속을 허용하고 포트 설정
ENV STREAMLIT_SERVER_PORT=8501            
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0      

# 컨테이너에서 사용할 포트 지정
EXPOSE 8501

# 컨테이너 시작 시 실행할 명령어 지정
CMD ["streamlit", "run", "app.py"]