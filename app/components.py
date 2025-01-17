import os
import time
import streamlit as st
import base64
import requests
import io
from pathlib import Path
from PIL import Image

# FastAPI 서버의 URL (여기서 localhost:8000은 FastAPI 서버가 실행되는 주소)
# 근데 여기 뭔가 수정이 필요함. 이런게 관리 되는건 좀 아닌거 같은데.
#3API_URL = "http://localhost:8000/transform_image/"
#GET_CONVERTED_API_URL = "http://localhost:8000/get_converted_image/"

API_URL = os.getenv("API_URL", "http://localhost:8000/transform_image/")
GET_CONVERTED_API_URL = os.getenv("GET_CONVERTED_API_URL", "http://localhost:8000/get_converted_image/")


# ===============================================
# 이미지 업로드 후 FastAPI 서버로 전송하는 함수
# ===============================================
def transform_image_to_backend(uploaded_file, model_name):
    """FastAPI 서버로 이미지를 전송하여 변환 요청"""
    # 파일 내용을 BytesIO로 변환
    file_bytes = io.BytesIO(uploaded_file.getvalue())
    files = {"file": ("image.png", file_bytes, "image/png")}
    data = {"model_name": model_name}  # 모델 이름 전달

    response = requests.post(API_URL, files=files, data=data)
    if response.status_code == 200:
        st.success("이미지 변환 요청 성공!")
        return response.json()  # 서버에서 반환된 파일명 정보 반환
    else:
        st.error(f"이미지 변환 요청 실패! 오류 메시지: {response.text}")
        return None    
    """
    files = {"file": uploaded_file}
    data = {"model_name": model_name}  # 모델 이름 전달

    response = requests.post(API_URL, files=files, data=data)
    if response.status_code == 200:
        st.success("이미지 변환 요청 성공!")
        return response.json()  # 서버에서 반환된 파일명 정보 반환
    else:
        st.error("이미지 변환 요청 실패! 오류")
        return None
    """

# ===============================================
# 요청 화면 (1번 화면): 사진 업로드와 사진 선택
# ===============================================
def show_request_screen():
    st.title("sosoPanda")

    # 모델 선택
    model_option = st.selectbox("사용할 모델을 선택하세요.", ["Model1", "Model2", "UGATIT"])

    # 사진 업로드
    uploaded_file = st.file_uploader("사진을 선택하세요.", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 업로드된 파일을 base64로 인코딩
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # 업로드된 이미지를 표시 (3:4 비율, 테두리 추가)
        st.markdown(
            f"""
            <div style="border: 5px solid pink; padding: 10px; 
            display: flex; justify-content: center; align-items: center; 
            width: 300px; height: 400px; margin: 0 auto;">
                <img src="data:image/png;base64,{img_base64}" 
                style="object-fit: cover; width: 100%; height: 100%;">
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.write("업로드된 이미지 미리보기")

    # 변환하기 버튼
    if st.button("변환하기"):
        if uploaded_file is None:
            # 사진이 선택되지 않은 경우 경고 메시지
            st.warning("변환할 사진을 선택하세요.")
        else:
            # 세션 상태에 필요한 데이터 저장
            st.session_state['step'] = 2  # 대기 화면으로 이동
            st.session_state['uploaded_file'] = uploaded_file  # 업로드된 파일 저장
            st.session_state['model_option'] = model_option  # 선택된 모델 저장

# ===============================================
# 대기 화면 (2번 화면): 프로그래스바와 대기 메시지
# ===============================================
def show_wait_screen():
    st.title("sosoPanda")
    st.write("예쁜 사진을 만들고 있어요. 잠시만 기다려주세요.")

    # 진행 바 (0% -> 100%)
    progress_bar = st.progress(0)
    for percent in range(100):
        progress_bar.progress(percent + 1)
        time.sleep(0.05)  # 약간의 지연 시간 추가

    print('uploaded_file123==>',st.session_state['uploaded_file'])

    # FastAPI 서버에 업로드된 파일을 전송
    result = transform_image_to_backend(
        st.session_state['uploaded_file'],
        st.session_state['model_option']
    )

    if result and "filename" in result:
        st.session_state['step'] = 3  # 결과 화면으로 이동
        st.session_state['converted_image'] = result["filename"]
        st.experimental_rerun()
    else:
        # 변환 실패 시 초기 화면으로 돌아가기
        st.error("이미지를 변환하는 데 실패했습니다.")
        st.session_state['step'] = 1
        st.experimental_rerun()

# ===============================================
# 결과 화면 (3번 화면): 변환된 사진과 저장/공유 버튼
# ===============================================
def show_result_screen():
    st.title("sosoPanda")
    
    # 첫 화면으로 돌아가는 버튼
    if st.button("처음으로"):
        st.session_state['step'] = 1

    # 변환된 이미지 표시
    if 'converted_image' in st.session_state:
        image_path = Path("storage/converted") / st.session_state['converted_image']

        # image_path를 문자열로 변환
        image_path_str = str(image_path)

        if os.path.exists(image_path):
            # 이미지를 열어서 3:4 비율로 크기 조정
            image = Image.open(image_path_str)
            width, height = image.size
            new_height = 400  # 세로 크기 고정
            new_width = int(width * (new_height / height))  # 비율에 맞게 가로 크기 조정
            image_resized = image.resize((new_width, new_height))

            # 이미지를 base64로 인코딩하여 HTML에서 사용할 수 있도록 변환
            buffered = io.BytesIO()
            image_resized.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # HTML로 이미지를 표시 (테두리 추가, 3:4 비율)
            st.markdown(
                f"""
                <div style="border: 5px solid pink; padding: 10px; 
                display: flex; justify-content: center; align-items: center; 
                width: 300px; height: 400px; margin: 0 auto;">
                    <img src="data:image/png;base64,{img_base64}" 
                    style="object-fit: cover; width: 100%; height: 100%;">
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 저장 버튼 (다운로드 기능)
            st.download_button(
                label="파일 저장",
                data=open(image_path_str, "rb").read(),
                file_name=st.session_state['converted_image'],
                mime="image/jpeg",
            )
        else:
            st.error(f"변환된 이미지를 불러오는 데 실패했습니다. {image_path_str}")
    else:
        st.error("변환된 이미지를 찾을 수 없습니다.")

    # 공유 버튼 (이메일로 공유하기)
    """
    col1, col2 = st.columns([1, 1])  # 두 개의 버튼을 한 줄로 배치
    with col1:
        if st.button("이메일로 공유"):
            share_url = f"mailto:?subject=변환된 이미지&body={st.session_state['converted_image']}"
            st.markdown(f"[이메일로 공유하기]({share_url})", unsafe_allow_html=True)

    with col2:
        if st.button("인스타그램 공유"):
            share_url = f"https://www.instagram.com/?url={st.session_state['converted_image']}"
            st.markdown(f"[인스타그램으로 공유하기]({share_url})", unsafe_allow_html=True)
    """
# ===============================================
# 배경 이미지를 설정하는 함수
# ===============================================
def add_background_image(image_path: str):
    """
    화면에 배경 이미지를 추가하는 함수
    :param image_path: 배경 이미지 경로 (예: "app/static/background.jpg")
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("file://{image_path}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )