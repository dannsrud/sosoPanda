import tensorflow as tf
import numpy as np
import cv2
import dlib
from models.UGATIT.UGATIT import UGATIT
from collections import namedtuple
import os

class UGATIT100 :
    def initialize_model(checkpoint_path):
        print("initialize_model : Start")
        Args = namedtuple("Args", [
            "light", "phase", "checkpoint_dir", "result_dir", "log_dir", "dataset", "augment_flag", "epoch",
            "iteration", "decay_flag", "decay_epoch", "gan_type", "batch_size", "print_freq", "save_freq",
            "lr", "ch", "adv_weight", "cycle_weight", "identity_weight", "cam_weight", "GP_ld", "smoothing",
            "n_res", "n_dis", "n_critic", "sn", "img_size", "img_ch", "sample_dir"
        ])

        args = Args(
            light=False, phase="test", checkpoint_dir="checkpoint", result_dir="results", log_dir="logs",
            dataset="selfie2anime", augment_flag=False, epoch=100, iteration=100000, decay_flag=False,
            decay_epoch=50, gan_type="lsgan", batch_size=1, print_freq=100, save_freq=1000, lr=0.0002, ch=64,
            adv_weight=1, cycle_weight=10, identity_weight=10, cam_weight=1000, GP_ld=10, smoothing=False,
            n_res=4, n_dis=6, n_critic=1, sn=True, img_size=256, img_ch=3, sample_dir="./samples"
        )

        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        model = UGATIT(sess, args=args)
        model.build_model()
        saver = tf.train.Saver()
        saver.restore(sess, checkpoint_path)
        print("Model loaded from:", checkpoint_path)
        return model, sess

    def preprocess_image(image_path):
        print('preprocess_image : Start')
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detector = dlib.get_frontal_face_detector()

        shape_predictor_path = os.path.join(
            "models",
            "UGATIT",
            "checkpoint",
            "shape_predictor_5_face_landmarks.dat"
        )
        #sp = dlib.shape_predictor("/models/UGATIT/checkpoint/shape_predictor_5_face_landmarks.dat")
        sp = dlib.shape_predictor(shape_predictor_path)
        dets = detector(img)
        if len(dets) == 0:
            raise Exception("No faces detected in the image")
        s = sp(img, dets[0])
        cropped_img = dlib.get_face_chip(img, s, size=256, padding=0.65)
        img_input = cv2.resize(cropped_img, (256, 256))
        img_input = np.expand_dims(img_input, axis=0)
        img_input = img_input / 127.5 - 1
        return img_input


    def generate_anime_image(model, sess, input_image, output_path):
        print('generate_anime_image:Start')
        output_image = sess.run(model.test_fake_B, feed_dict={model.test_domain_A: input_image})
        output_image = (output_image + 1) * 127.5
        output_image = output_image.astype(np.uint8).squeeze()
        cv2.imwrite(output_path, cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))
        print("Anime image saved to:", output_path)


    if __name__ == "__main__":
        #checkpoint_path = "/models/UGATIT/checkpoint/UGATIT.model-1000000"
        #input_image_path = "/models/UGATIT/bp_rose.jpg"
        #output_image_path = "/models/UGATIT/output_image.jpg"
        
        #base_dir = "D:/Projects/WebtoonAI"
        checkpoint_path = os.path.join(
            #base_dir,
            "models",
            "UGATIT",
            "checkpoint",
            "UGATIT.model-1000000"
        )
        input_image_path = os.path.join(
            "models",
            "UGATIT",
            "bp_rose.jpg"
        )    
        
        output_image_path = os.path.join(
            "models",
            "UGATIT",
            "output_image.jpg"
        )
        
        print('=====================================')
        print('checkpoint_path===',checkpoint_path)
        print('input_image_path===',input_image_path)
        print('output_image_path===',output_image_path)
        print('=====================================')

        model, sess = initialize_model(checkpoint_path)
        input_image = preprocess_image(input_image_path)
        generate_anime_image(model, sess, input_image, output_image_path)
        

