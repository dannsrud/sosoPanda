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
API_URL = os.getenv("API_URL", "http://localhost:8000/transform_image/")
#GET_CONVERTED_API_URL = os.getenv("GET_CONVERTED_API_URL", "http://localhost:8000/get_converted_image/")


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


# ===============================================
# 요청 화면 (1번 화면 + 2번 화면 ) : 사진 업로드와 사진 선택
#   (대기모드를 모달로 띄우기 위해 하나로 합쳤음.)
# ===============================================
def show_request_screen():
    st.title("sosoPanda")

    # 모델 선택
    model_option = st.selectbox("사용할 모델을 선택하세요.", ["Model1", "UGATIT_50", "UGATIT_100"])

    # 사진 업로드
    uploaded_file = st.file_uploader("사진을 선택하세요.", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 업로드된 파일을 base64로 인코딩
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # 업로드된 이미지를 표시 (1:1 정사각형 비율, 테두리 추가)
        st.markdown(
            f"""
            <div style="border: 5px solid pink; padding: 10px; 
            display: flex; justify-content: center; align-items: center; 
            width: 300px; height: 300px; margin: 0 auto;">
                <img src="data:image/png;base64,{img_base64}" 
                style="object-fit: cover; width: 100%; height: 100%;">
            </div>
            """,
            unsafe_allow_html=True
        )


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

            # 대기 화면 모달 표시
            st.markdown(
                """
                <div id="modal" style="
                    position: fixed; 
                    top: 0; 
                    left: 0; 
                    width: 100%; 
                    height: 100%; 
                    background-color: rgba(255, 255, 255, 0.8);
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    z-index: 9999;">
                    <div style="
                        background-color: white; 
                        padding: 30px 40px; 
                        border-radius: 10px; 
                        text-align: center;
                        width: 400px;">
                        <div class="loading-text">
                            <span>사</span>
                            <span>진</span>
                            <span>변</span>
                            <span>환</span>
                            <span>중</span>
                            <span>.</span>
                            <span>.</span>
                            <span>.</span>
                        </div>
                        <p style="margin: 10px 0;">예쁜 사진을 만들고 있어요. 잠시만 기다려주세요.</p>
                        <div id="progress-container" style="width: 100%; margin-top: 15px;">
                            <div id="progress-bar" style="width: 10%; height: 6px; background-color: #FFA500; border-radius: 10px;"></div>
                        </div>
                    </div>
                </div>

                <style>
                .loading-text {
                    margin: 0;
                    font-size: 28px;
                    white-space: nowrap;  /* 줄바꿈 방지 */
                }

                .loading-text span {
                    display: inline-block;
                    animation: flip 2s infinite;
                    animation-delay: calc(.2s * var(--i));
                }

                @keyframes flip {
                    0%, 80% {
                        transform: rotateY(360deg);
                        color:rgb(240, 145, 77);  /* 오렌지 계열 글자색 */
                        background-color:rgb(250, 238, 215);  /* 연한 오렌지 배경색 */
                        padding: 2px 8px;
                        border-radius: 6px;
                        font-weight: 900;
                    }
                    40% {
                        color: #333;
                        background-color: transparent;
                    }
                }

                .loading-text span:nth-child(1) { --i: 1; }
                .loading-text span:nth-child(2) { --i: 2; }
                .loading-text span:nth-child(3) { --i: 3; }
                .loading-text span:nth-child(4) { --i: 4; }
                .loading-text span:nth-child(5) { --i: 5; }
                .loading-text span:nth-child(6) { --i: 6; }
                .loading-text span:nth-child(7) { --i: 7; }
                .loading-text span:nth-child(8) { --i: 8; }
                </style>

                <script>
                    let progressBar = document.getElementById('progress-bar');
                    let progress = 0;
                    let interval = setInterval(() => {
                        progress += 1;
                        progressBar.style.width = progress + '%';
                        if (progress >= 100) {
                            clearInterval(interval);
                            document.getElementById('modal').style.display = 'none';
                        }
                    }, 50);
                </script>
                """,
                unsafe_allow_html=True
            )

            # Streamlit progress bar for waiting time simulation
            '''
            progress_bar = st.progress(0)
            for percent in range(100):
                progress_bar.progress(percent + 1)
                time.sleep(0.05)  # Simulating processing time
            '''

            # FastAPI 서버에 업로드된 파일을 전송
            result = transform_image_to_backend(
                st.session_state['uploaded_file'],
                st.session_state['model_option']
            )

            print('===========result===========',result)

            if result :
                # 원본 파일명과 변환된 파일명을 세션에 저장
                st.session_state['original_filename'] = result["original_filename"]
                st.session_state['converted_image'] = result["converted_filename"]
                st.session_state['step'] = 3
                st.experimental_rerun()
            else:
                # 변환 실패 시 초기 화면으로 돌아가기
                st.error("이미지를 변환하는 데 실패했습니다.")
                st.session_state['step'] = 1
                st.experimental_rerun()


# 두 이미지 모두 256x256으로 리사이즈
def process_image(image_path):
    image = Image.open(image_path)
    image_resized = image.resize((256, 256))
    buffered = io.BytesIO()
    image_resized.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# ===============================================
# 결과 화면 (3번 화면): 변환된 사진과 저장/공유 버튼 - 변경중
# ===============================================
def show_result_screen():
    st.title("sosoPanda")
    
    if st.button("처음으로"):
        st.session_state['step'] = 1

    # 두 이미지를 나란히 표시할 컨테이너 생성
    if 'converted_image' in st.session_state:
        # 원본 이미지 경로
        original_path = os.path.join("storage", "uploads", st.session_state['original_filename'])
        # 변환된 이미지 경로
        converted_path = os.path.join("storage", "converted", st.session_state['converted_image'])
       
        print('------original_path::',original_path)
        print('------converted_path::',converted_path)   

        print(f"Original file exists: {os.path.exists(original_path)}")
        print(f"Converted file exists: {os.path.exists(converted_path)}")
        
        try: 
            if os.path.exists(original_path) and os.path.exists(converted_path):
                original_base64 = process_image(original_path)
                converted_base64 = process_image(converted_path)

                # HTML로 두 이미지를 나란히 표시
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; gap: 20px;">
                        <div style="border: 5px solid pink; padding: 20px; width: 300px;">
                            <p style="text-align: center; margin: 0 0 20px 0; font-size: 18px; font-weight: bold;">원본 이미지</p>
                            <div style="width: 256px; height: 256px; margin: 0 auto;">
                                <img src="data:image/png;base64,{original_base64}" 
                                style="width: 100%; height: 100%; object-fit: contain;">
                            </div>
                        </div>
                        <div style="border: 5px solid pink; padding: 20px; width: 300px;">
                            <p style="text-align: center; margin: 0 0 20px 0; font-size: 18px; font-weight: bold;">변환된 이미지</p>
                            <div style="width: 256px; height: 256px; margin: 0 auto;">
                                <img src="data:image/png;base64,{converted_base64}" 
                                style="width: 100%; height: 100%; object-fit: contain;">
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # 저장 버튼과 위 내용 사이 여백 추가
                st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
                
                # 저장 버튼
                with open(converted_path, "rb") as file:
                    st.download_button(
                        label="파일 저장",
                        data=file.read(),
                        file_name=st.session_state['converted_image'],
                        mime="image/jpeg",
                    )
            else:
                st.error("원본 또는 변환된 이미지를 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")
    else:
        st.error("변환된 이미지를 찾을 수 없습니다.")


# ===============================================
# 배경 이미지를 설정하는 함수
# ===============================================
def add_background_image(image_path: str):
    """
    화면에 배경 이미지를 추가하는 함수
    :param image_path: 배경 이미지 경로 (예: "app/static/background.jpg")
    """
    image_path = 'app\static\background.jpg' 
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