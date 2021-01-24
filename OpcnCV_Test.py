from PIL import Image
import cv2
import numpy as np
import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config = config)

saved = load_model("Models/save_ckp_frozen.h5")

class fashion_tools(object):
    def __init__(self, imageid, model, version=1.1):
        self.imageid = imageid
        self.model = model
        self.version = version

    def get_dress(self, stack = False):
        name = self.imageid
        file = cv2.imread(name)
        file = tf.image.resize_with_pad(file, target_height=512, target_width=512)
        rgb = file.numpy()
        file = np.expand_dims(file, axis=0) / 255.
        seq = self.model.predict(file)
        seq = seq[3][0, :, :, 0]
        seq = np.expand_dims(seq, axis=-1)
        c1x = rgb * seq
        c2x = rgb * (1 - seq)
        cfx = c1x + c2x
        dummy = np.ones((rgb.shape[0], rgb.shape[1], 1))
        rgbx = np.concatenate((rgb, dummy * 255), axis=-1)
        rgbs = np.concatenate((cfx, seq * 255.), axis=-1)
        if stack:
            stacked = np.hstack((rgbx, rgbs))
            return stacked
        else:
            return rgbs

    def get_patch(self):
        return None

def Back_subtraction(image_name):
    img = Image.open("Image/" + image_name + ".png")
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    cutOff = 150

    for item in datas:
        if item[0] >= cutOff and item[1] >= cutOff and item[2] >= cutOff:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("Image/" + image_name + "_Background_Substraction.png", "PNG")

def Video_Capture():
    print(tf.__version__)
    global image_count
    image_count = 0
    image_name = "image"
    cap = cv2.VideoCapture(0)
    cap.set(3, 720)
    cap.set(4, 1080)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Video', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == ord('a'):
            image_count = image_count + 1
            image_name = image_name + str(image_count)
            cv2.imwrite("Image/" + image_name + ".png", frame)
            print("Image Save!!")
        elif k == ord('s'):
            if (image_name == "image"):
                print("Error!!!!!")
            Back_subtraction("out")
            print("Back Subtraction")
            image_name = "image"
        elif k == ord('d'):
            image_name_2 = "Image/" + image_name + ".png"
            api = fashion_tools(image_name_2, saved)
            print("Clothes Detection")
            image_ = api.get_dress(True)
            cv2.imwrite("Image/out.png", image_)
    cap.release()
    cv2.destroyAllWindows()

Video_Capture()