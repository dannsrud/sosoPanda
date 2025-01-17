# 스트림릿 
import streamlit as st
# 페이지 설정을 가장 먼저 해야 함
st.set_page_config(
    page_title="쏘쏘판다",
    layout="wide"  
)

# 나머지 임포트
from PIL import Image
import os
from models.model_utils import ModelManager

# 모델 매니저 초기화
model_dir = os.path.join(os.path.dirname(__file__), 'models')
model_manager = None

try:
    model_manager = ModelManager(model_dir)
except Exception as e:
    st.error(f"모델 로드 중 오류 발생: {str(e)}")

def main():
    # 타이틀 정하기.
    st.title("내 사진을 웹툰 캐릭터로!")
    
    # 두 컬럼으로 나누기
    col1, col2 = st.columns(2)
    
    # 왼쪽 컬럼: 입력 이미지
    with col1:
        st.subheader("입력 이미지")
        # 파일 업로더 생성
        uploaded_file = st.file_uploader(
            "이미지를 업로드해주세요",
            type=['png', 'jpg', 'jpeg']
        )
        
        # 업로드된 이미지 표시
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="입력 이미지")
            
            # 변환 버튼
            if st.button("변환하기"):
                if model_manager is None:
                    st.error("모델이 로드되지 않았습니다.")
                else:
                    try:
                        # 실제 변환 로직 실행
                        with st.spinner("변환 중..."):
                            output_image = model_manager.transform_to_webtoon(image)
                            st.session_state.output_image = output_image
                    except Exception as e:
                        st.error(f"이미지 변환 중 오류 발생: {str(e)}")
    
    # 오른쪽 컬럼: 출력 이미지
    with col2:
        st.subheader("변환된 이미지")
        # 변환된 이미지가 있으면 표시
        if 'output_image' in st.session_state:
            st.image(
                st.session_state.output_image,
                caption="변환된 이미지"
            )

if __name__ == "__main__":
    main()