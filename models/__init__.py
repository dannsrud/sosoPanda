"""
쏘쏘판다 웹툰 변환 모델 패키지

이 패키지는 실제 사진을 웹툰 스타일로 변환하는 AI 모델과 관련 유틸리티를 제공합니다.

주요 모듈:
- pix2pix: Pix2Pix 모델 구현
- model_utils: 모델 관리 유틸리티

사용 예시:
    from models.model_utils import ModelManager
    
    # 모델 매니저 초기화
    manager = ModelManager('path/to/model/dir')
    
    # 이미지 변환
    output_image = manager.transform_to_webtoon(input_image)
"""

from .model_utils import ModelManager
from .pix2pix import Pix2PixModel

__all__ = ['ModelManager', 'Pix2PixModel']
