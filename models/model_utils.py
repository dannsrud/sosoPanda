"""
웹툰 변환 모델 관리 유틸리티

이 모듈은 웹툰 변환 모델의 로딩과 관리를 담당합니다.
ModelManager 클래스를 통해 모델의 생명주기를 관리하고,
간단한 인터페이스를 제공하여 이미지 변환을 쉽게 수행할 수 있게 합니다.

주요 기능:
- 모델 파일 자동 로드
- 모델 상태 관리
- 간단한 이미지 변환 인터페이스 제공
- 에러 처리

사용 예시:
    manager = ModelManager('path/to/model/dir')
    output_image = manager.transform_to_webtoon(input_image)
"""

import os
from typing import Optional
from PIL import Image
from .pix2pix import Pix2PixModel

class ModelManager:
    """
    웹툰 변환 모델 관리 클래스
    
    이 클래스는 웹툰 변환 모델의 로딩과 관리를 담당합니다.
    모델 파일을 자동으로 로드하고, 이미지 변환을 위한 간단한 인터페이스를 제공합니다.
    
    Attributes:
        model_dir (str): 모델 파일이 저장된 디렉토리 경로
        model (Optional[Pix2PixModel]): 로드된 Pix2Pix 모델 인스턴스
    """

    def __init__(self, model_dir: str):
        """
        ModelManager 초기화
        
        Args:
            model_dir (str): 모델 파일이 저장된 디렉토리 경로
            
        Raises:
            FileNotFoundError: 모델 디렉토리를 찾을 수 없는 경우
        """
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"모델 디렉토리를 찾을 수 없습니다: {model_dir}")
        
        self.model_dir = model_dir
        self.model: Optional[Pix2PixModel] = None
        self.load_model()

    def load_model(self):
        """
        웹툰 변환 모델 로드
        
        'vgg.pth' 파일을 찾아 Pix2Pix 모델을 로드합니다.
        
        Raises:
            FileNotFoundError: 모델 파일을 찾을 수 없는 경우
            Exception: 모델 로드 중 오류가 발생한 경우
        """
        model_path = os.path.join(self.model_dir, 'src', 'models', 'lpips', 'weights', 'v0.1', 'vgg.pth')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")
        
        try:
            self.model = Pix2PixModel(model_path)
        except Exception as e:
            raise Exception(f"모델 로드 중 오류가 발생했습니다: {str(e)}")

    def transform_to_webtoon(self, image: Image.Image) -> Image.Image:
        """
        실제 사진을 웹툰 스타일로 변환
        
        입력된 이미지를 웹툰 스타일로 변환합니다.
        변환 전에 모델이 제대로 로드되었는지 확인합니다.
        
        Args:
            image (PIL.Image): 변환할 원본 이미지
            
        Returns:
            PIL.Image: 웹툰 스타일로 변환된 이미지
            
        Raises:
            RuntimeError: 모델이 로드되지 않은 경우
            Exception: 이미지 변환 중 오류가 발생한 경우
        """
        if self.model is None:
            raise RuntimeError("모델이 로드되지 않았습니다")
        
        try:
            return self.model.transform_image(image)
        except Exception as e:
            raise Exception(f"이미지 변환 중 오류가 발생했습니다: {str(e)}")
