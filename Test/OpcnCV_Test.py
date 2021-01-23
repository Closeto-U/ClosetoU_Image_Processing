from PIL import Image
import cv2
import numpy as np
import datetime

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
        elif k == 26:
            image_count = image_count + 1
            image_name = image_name + str(image_count)
            cv2.imwrite("Image/" + image_name + ".png", frame)
            print("Image Save!!")
        elif k == 24:
            if (image_name == "image"):
                print("Error!!!!!")
            Back_subtraction(image_name)
            print("Back Subtraction")
            image_name = "image"
    cap.release()
    cv2.destroyAllWindows()

Video_Capture()