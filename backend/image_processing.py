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

tf.logging.set_verbosity(tf.logging.ERROR)


CONVERTED_DIR = "storage/converted"

converted_filename = "colab.png"

# ===============================================
# Pix2Pix 모델 처리 (예제입니다)
# ===============================================
def process_pix2pix(image_path: str) -> str:
    '''
    # Pix2Pix 모델 로드 및 처리 로직
    from models.pix2pix import Pix2PixModel
    model = Pix2PixModel.load("models/pix2pix.pth")
    
    with Image.open(image_path) as img:
        output_image = model.transform(img)
    
    converted_filename = f"converted_pix2pix_{os.path.basename(image_path)}"
    output_path = os.path.join(CONVERTED_DIR, converted_filename)
    output_image.save(output_path)
    '''

    # storage/converted/colab.png 파일명을 강제로 반환
    output_path = os.path.abspath(os.path.join(CONVERTED_DIR, converted_filename))

    # 해당 경로에 파일이 없으면 오류 방지를 위해 확인 후 생성
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{output_path} 파일이 존재하지 않습니다. 해당 파일을 먼저 생성하세요.")

    return output_path
    

def process_pix2pix2(image_path: str) -> str:
    # Pix2Pix 모델 로드
    model = torch.load("models/pix2pix.pth")
    model.eval()

    # 이미지 전처리
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 이미지 로드 및 변환
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)

    # 모델 추론
    with torch.no_grad():
        output = model(img_tensor)

    # 결과 이미지 생성
    output_img = transforms.ToPILImage()(output.squeeze(0) * 0.5 + 0.5)

    # 결과 저장
    converted_filename = f"converted_pix2pix_{os.path.basename(image_path)}"
    output_path = os.path.join(CONVERTED_DIR, converted_filename)
    output_img.save(output_path)

    return output_path


# ===============================================
# StyleGAN 모델 처리 (예제입니다)
# ===============================================
def process_stylegan(image_path: str) -> str:
    '''
    # StyleGAN 모델 로드 및 처리 로직
    from models.stylegan import StyleGANModel
    model = StyleGANModel.load("models/stylegan.pkl")
    
    with Image.open(image_path) as img:
        output_image = model.transform(img)
    
    converted_filename = f"converted_stylegan_{os.path.basename(image_path)}"
    output_path = os.path.join(CONVERTED_DIR, converted_filename)
    output_image.save(output_path)
    '''
    # storage/converted/colab.png 파일명을 강제로 반환
    output_path = os.path.abspath(os.path.join(CONVERTED_DIR, converted_filename))

    # 해당 경로에 파일이 없으면 오류 방지를 위해 확인 후 생성
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{output_path} 파일이 존재하지 않습니다. 해당 파일을 먼저 생성하세요.")

    return output_path


def process_stylegan2(image_path: str) -> str:
    # StyleGAN 모델 로드
    model = torch.load("models/stylegan.pth")
    model.eval()

    # 이미지 전처리
    transform = transforms.Compose([
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 이미지 로드 및 변환
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)

    # 모델 추론
    with torch.no_grad():
        output = model(img_tensor)

    # 결과 이미지 생성
    output_img = transforms.ToPILImage()(output.squeeze(0) * 0.5 + 0.5)

    # 결과 저장
    converted_filename = f"converted_stylegan_{os.path.basename(image_path)}"
    output_path = os.path.join(CONVERTED_DIR, converted_filename)
    output_img.save(output_path)

    return output_path


# ===============================================
# U-GAT-IT 모델 처리
# ===============================================
def process_ugatit(image_path: str) -> str:
    # U-GAT-IT 모델 로드
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    checkpoint_path = os.path.join(BASE_DIR, 'models', 'UGATIT_100', 'checkpoint', 'UGATIT.model-1000000')

    # 그래프 초기화
    tf.reset_default_graph()
    
    # 세션 설정
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    
    with tf.Session(config=config) as sess:
        # 메타그래프 로드
        saver = tf.train.import_meta_graph(checkpoint_path + '.meta')
        # 체크포인트 복원
        saver.restore(sess, checkpoint_path)
        
        # 그래프 가져오기
        graph = tf.get_default_graph()

    # 이미지 전처리
    img = Image.open(image_path).convert('RGB')
    img = img.resize((256, 256), Image.LANCZOS)
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)
    img = img/127.5 - 1  # normalize to [-1, 1]

    # 모델 추론
    graph = tf.get_default_graph()
    input_tensor = graph.get_tensor_by_name("input:0")
    output_tensor = graph.get_tensor_by_name("output:0")
    output = sess.run(output_tensor, feed_dict={input_tensor: img})

    # 결과 이미지 생성
    output = (output + 1) * 127.5  # denormalize to [0, 255]
    output = output.astype(np.uint8)
    output_img = Image.fromarray(output[0])

    # 결과 저장
    converted_filename = f"converted_ugatit_{os.path.basename(image_path)}"
    output_path = os.path.join(CONVERTED_DIR, converted_filename)
    output_img.save(output_path)

    return output_path

# ===============================================
# 모델 이름에 따라 적절한 함수 호출
# ===============================================
def process_image(image_path: str, model_name: str) -> str:
    # 모델 이름에 따른 함수 매핑
    model_functions = {
        "Model1": process_pix2pix,
        "Model2": process_stylegan,
        "UGATIT": process_ugatit
    }

    # 모델이 지원되는지 확인
    if model_name not in model_functions:
        raise ValueError(f"지원되지 않는 모델: {model_name}")

    # 해당 모델 함수 호출
    return model_functions[model_name](image_path)

