import streamlit as st
import torch
from PIL import Image
import os
import sys
import numpy as np
from torchvision import transforms

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.set_page_config(
    page_title="Cartoon StyleGAN",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Cartoon StyleGAN")
st.markdown("""
이 앱은 실제 사진을 만화 스타일로 변환해주는 서비스입니다.
업로드한 이미지를 선택한 스타일로 변환할 수 있습니다.
""")

# 파일 업로더
uploaded_file = st.file_uploader(
    "이미지 업로드",
    type=["png", "jpg", "jpeg"],
    help="변환하고 싶은 이미지를 업로드하세요."
)

if uploaded_file is not None:
    # 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)
    
    st.info("현재 CPU 버전으로 개발 중입니다. 곧 이미지 변환 기능이 추가될 예정입니다.")
