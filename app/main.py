# app/main.py
import logging
import os
import sys
import streamlit as st
from app.components import show_request_screen, show_wait_screen, show_result_screen # 상대 경로로 함수 임포트

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# app.log파일에 쌓는 방법도 찾아봐야함.

# 환경 변수 확인
is_local = os.getenv("LOCAL_ENV", "false").lower() == "true"

if is_local:
    logger.info("logger :: Running in local")
    # 로컬 환경일 경우 경로 추가
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
else:
    logger.info("logger ::Running in GCP")

# ===============================================
# 화면 분기
# ===============================================
def main():

    # 배경 이미지 추가
    #add_background_image("app/static/background.jpg")

    # Streamlit에서 사용자가 현재 보는 화면을 세션 상태로 관리
    if 'step' not in st.session_state:
        st.session_state['step'] = 1  # 기본적으로 1번 화면부터 시작
    
    # 1번 화면 (요청 화면)
    if st.session_state['step'] == 1:
        show_request_screen()
    
    # 2번 화면 (대기 화면)
    elif st.session_state['step'] == 2:
        show_wait_screen()
    
    # 3번 화면 (결과 화면)
    elif st.session_state['step'] == 3:
        show_result_screen()

if __name__ == "__main__":
    main()