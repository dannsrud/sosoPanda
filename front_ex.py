# 스트림릿 
import streamlit as st
# 파이썬에서 이미지를 처리하기 위한 라이브러리!
from PIL import Image

# Streamlit 세션 상태에서 현재 페이지를 추적하기 위한 초기 설정
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

# 다른 페이지로 이동하는 함수
def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()


def main_page():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="쏘쏘판다",
        layout="wide"  
    )
    
    # 타이틀 정하기.
    st.title("내 사진을 웹툰 캐릭터로!")

    # 프로젝트 소개하는 서브 페이지로 이동
    if st.button('SosoPanda AI'):
        navigate_to('sub')

    
    # 두 컬럼으로 나누기
    col1, col2 = st.columns(2)
    
    # 왼쪽 컬럼: 입력 이미지
    with col1:
        st.subheader("입력 이미지")
        # 파일 업로더 생성
        uploaded_file = st.file_uploader(
            "이미지를 업로드해주세요",
            type=['png', 'jpg', 'jpeg'] # 여기에 확장자 관련된 것! 필요하다 추가해서 넣으면 될 거 같아용!
        )
        
        # 업로드된 이미지 표시
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="입력 이미지")
            
            # 변환 버튼
            if st.button("변환하기"):
                # TODO: 여기에 실제 변환 로직 구현
                with st.spinner("변환 중..."):
                    # 임시로 같은 이미지를 출력
                    st.session_state.output_image = image
    
    # 오른쪽 컬럼: 출력 이미지
    with col2:
        st.subheader("변환된 이미지")
        # 변환된 이미지가 있으면 표시
        if 'output_image' in st.session_state:
            st.image(
                st.session_state.output_image,
                caption="변환된 이미지"
            )
            # 이미지 저장 버튼.
            st.download_button(label='저장하기', data = st.session_state.output_image,
                               file_name='webtoon_img.png')

if __name__ == "__main__":
    main_page()

# 서브 페이지 내용 정의
def sub_page():
    st.title('SosoPanda AI')
    st.write('제작 : 우문경, 임나현, 강상우, 이경옥, 송다영')
    if st.button('메인 페이지로 돌아가기'):
        navigate_to('main')

# 페이지 네비게이션 로직
if st.session_state['page'] == 'main':
    main_page()
elif st.session_state['page'] == 'sub':
    sub_page()
