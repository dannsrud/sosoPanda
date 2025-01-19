# backend/image_processing.py

from PIL import Image
import os
import torch
import torchvision.transforms as transforms
import tensorflow as tf
import numpy as np
#import cv2
#import dlib
#import matplotlib.pyplot as pl
#from glob import glob
#from UGATIT_noargs import UGATIT

#tf.logging.set_verbosity(tf.logging.ERROR)
import logging
logging.getLogger().setLevel(logging.ERROR)  # WARNING 레벨 이하의 메시지 숨김


CONVERTED_DIR = "storage/converted"
converted_filename = "colab.png"

# ===============================================
# 변환시 고유한 파일명 만들기 (UUID + 타임스탬프)
# ===============================================
import uuid
from datetime import datetime

def generate_unique_filename() -> str:
    # UUID와 현재 시간 조합
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{unique_id}_{timestamp}.png"
    return unique_filename

# ===============================================
# Pix2Pix 모델 처리 (예제입니다)
# ===============================================
def process_CycleGAN(image_path: str, output_path: str) -> str:
    
    # storage/converted/colab.png 파일명을 강제로 반환
    output_path = os.path.abspath(os.path.join(CONVERTED_DIR, converted_filename))

    # 해당 경로에 파일이 없으면 오류 방지를 위해 확인 후 생성
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{output_path} 파일이 존재하지 않습니다. 해당 파일을 먼저 생성하세요.")

    return output_path
    

# ===============================================
# U-GAT-IT 50에에폭 모델 처리
#    UGATIT-50 모델을 사용하여 이미지를 처리하는 함수
#    Args:
#        image_path (str): 원본 이미지 경로
#        output_path (str): 변환된 이미지 저장 경로
#    Returns:
#        output_path (str): 변환된 이미지 저장 경로
# ===============================================
def process_ugatit_50(image_path: str, output_path: str) -> str:
    print('START :: image_processing.py::process_ugatit_50')
    """
    UGATIT-50 모델을 사용하여 이미지를 처리하는 함수
    """
    import os
    from models.UGATIT.run_model_50 import UGATIT50
        
    try: 
        # Model initialization
        checkpoint_path = os.path.join(
            "models",
            "UGATIT",
            "checkpoint_50",
            "UGATIT.model-500001"
        )
        # 모델 초기화 체크
        model, sess = UGATIT50.initialize_model(checkpoint_path)
        if model is None or sess is None:
            raise ValueError("Model initialization failed")

        # Preprocess input image
        # 이미지 전처리 체크
        input_image = UGATIT50.preprocess_image(image_path)
        if input_image is None:
            raise ValueError("Image preprocessing failed")
    
        # storage/converted/colab.png 파일명을 강제로 반환

        unique_filename = generate_unique_filename()
        output_path = os.path.join(
            "storage",
            "converted",
            unique_filename
        )
        
        # Generate anime image
        # 이미지 생성 체크
        result = UGATIT50.generate_anime_image(model, sess, input_image, output_path)
        if result is None:
            raise ValueError("Image generation failed")
        
        # 결과 파일 존재 여부 체크
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output file not found: {output_path}")

        # Return the output image path
        return output_path
    except Exception as e:
        print(f"Error in process_ugatit_100: {str(e)}")
        raise ValueError(f"Image processing failed: {str(e)}")

# ===============================================
# U-GAT-IT 모델 처리
#    UGATIT-100 모델을 사용하여 이미지를 처리하는 함수
#    Args:
#        image_path (str): 원본 이미지 경로
#        output_path (str): 변환된 이미지 저장 경로
#    Returns:
#        output_path (str): 변환된 이미지 저장 경로
# ===============================================
def process_ugatit_100(image_path: str, output_path: str) -> str:
    print('START :: image_processing.py::process_ugatit_100')
    """
    UGATIT-100 모델을 사용하여 이미지를 처리하는 함수
    """
    try:
        import os
        from models.UGATIT.run_model_100 import UGATIT100

        # Model initialization
        checkpoint_path = os.path.join(
            "models",
            "UGATIT",
            "checkpoint_100",
            "UGATIT.model-1000000"
        )

        # 모델 초기화 체크
        model, sess = UGATIT100.initialize_model(checkpoint_path)
        if model is None or sess is None:
            raise ValueError("Model initialization failed")

        # Preprocess input image
        # 이미지 전처리 체크
        input_image = UGATIT100.preprocess_image(image_path)
        if input_image is None:
            raise ValueError("Image preprocessing failed")
    
        # storage/converted/colab.png 파일명을 강제로 반환

        unique_filename = generate_unique_filename()
        output_path = os.path.join(
            "storage",
            "converted",
            unique_filename
        )
        
        # Generate anime image
        # 이미지 생성 체크
        result = UGATIT100.generate_anime_image(model, sess, input_image, output_path)
        if result is None:
            raise ValueError("Image generation failed")
        
        # 결과 파일 존재 여부 체크
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output file not found: {output_path}")

        # Return the output image path
        return output_path
    except Exception as e:
        print(f"Error in process_ugatit_100: {str(e)}")
        raise ValueError(f"Image processing failed: {str(e)}")


# ===============================================
# 모델 이름에 따라 적절한 함수 호출
#    Args:
#        image_path (str): 원본 이미지 경로
#        model_name (str): 선택한 모델 이름
#    Returns:
#        output_path (str): 변환된 이미지 저장 경로
# ===============================================
def process_image(image_path: str, model_name: str, output_path: str) -> str:
    """
    모델 이름에 따라 적절한 이미지 처리 함수를 호출하는 함수
    """
    # 모델 이름에 따른 함수 매핑
    model_functions = {
        "Model1": process_CycleGAN,         # CycleGAN 모델 처리 함수
        "UGATIT_50": process_ugatit_50,     # StyleGAN 모델 처리 함수
        "UGATIT_100": process_ugatit_100    # UGATIT-100 모델 처리 함수
    }

    # 모델이 지원되는지 확인
    if model_name not in model_functions:
        raise ValueError(f"지원되지 않는 모델: {model_name}")

    # 해당 모델 처리 함수 호출
    return model_functions[model_name](image_path, output_path)


