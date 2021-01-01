import cv2
from PIL import Image

img = Image.open('clothes.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
cutOff = 190

for item in datas:
    if item[0] >= cutOff and item[1] >= cutOff and item[2] >= cutOff:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("Background_test.png", "PNG")