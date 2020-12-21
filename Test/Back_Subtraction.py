import cv2
import numpy as np

def Back_Subtraction():
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 320)

    mog = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()
        fgmask = mog.apply(frame)

        cv2.imshow('mask', fgmask)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()