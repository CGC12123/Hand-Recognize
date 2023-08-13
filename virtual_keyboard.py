import cv2
from hand_recognize_class import HandDetector
import numpy as np
import cvzone
import time
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4,720)

detector = HandDetector(detectionCon = 0.8)
keyboard = Controller()

class Button():
    def __init__(self, pos, text, size = [100,100]):
        self.pos = pos
        self.text = text
        self.size = size

# 定义键盘并显示
buttonList = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([120*j + 50, 130 * i + 50], key))

# 将键盘输出到画面上的函数
def drawALL(img, buttonList):
    # 绘制实体矩形
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 25, 25), cv2.FILLED)
        cvzone.cornerRect(img, (x, y, w, h), 20, rt = 0)
        cv2.putText(img, button.text, (x + 32, y + 71), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
    # # 绘制透明矩形
    # imgNew = np.zeros_like(img, np.uint8)
    # for button in buttonList:
    #     x, y = button.pos
    #     w, h = button.size
    #     cv2.rectangle(imgNew, button.pos, (x + w, y + h), (255, 25, 25), cv2.FILLED)
    #     cvzone.cornerRect(imgNew, (x, y, w, h), 20, rt = 0)
    #     cv2.putText(imgNew, button.text, (x + 23, y + 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
            
    #     out = img.copy()
    #     alpha = 0.1 # 透明度
    #     mask = imgNew.astype(bool)
    #     out[mask] = cv2.addWeighted(img, alpha, img, 1 - alpha, 0)[mask]

    return img


finalText = ""
while True:
    ret, img = cap.read()

    allHands, img = detector.findHands(img)
    lmList = detector.findPositions(img)

    img = drawALL(img, buttonList) # 画键盘

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w,h = button.size

            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 120, 25), cv2.FILLED)
                cv2.putText(img, button.text, (x + 23, y + 75), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(lmList[8], lmList[12], img = None) # 得到食指与中指指尖的距离l
                # print(l)
                # 当检测到为点击时
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (25, 200, 25), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 23, y + 75), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    time.sleep(0.15)
    cv2.rectangle(img, (60, 440), (1000, 520), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (70, 505), cv2.FONT_HERSHEY_PLAIN, 5, (150, 5, 50), 5)
        

    cv2.imshow("img", img)
    cv2.waitKey(1)