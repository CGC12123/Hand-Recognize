import cv2
from hand_recognize_class import HandDetector
import cvzone
import numpy as np

class DragRect():
    def __init__(self, posCenter, size = [100, 100]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        # 若手指在矩形内
        if cx-w//2 < cursor[1] < cx+w//2 and cy-h//2 < cursor[2] < cy+h//2:
            id, cx, cy = cursor
            self.posCenter = cx, cy
            self.size = w, h

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon = 0.8)
    rectList = []
    for x in range(3):
        rectList.append(DragRect([x*250 + 50, 50]))
    colorR = 255, 0, 255

    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        allHands, img = detector.findHands(img)
        lmList = detector.findPositions(img)

        if lmList:
            cursor = lmList[8]

            l, _, _ = detector.findDistance(lmList[8], lmList[12], img = None)
            # print(l) # 测试欲识别到的距离
            # print(cursor[1], cursor[2])
            if l < 30:
                for rect in rectList:
                    rect.update(cursor)

        # # 画出实体矩形
        # for rect in rectList:
        #     cx, cy = rect.posCenter
        #     w, h = rect.size
        #     cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
        #     cvzone.cornerRect(img, (cx-w//2, cy-h//2, w, h), 20, rt = 0)
        
        # cv2.imshow("img", img)
        # cv2.waitKey(1)


        # 画出半透明矩形
        imgNew = np.zeros_like(img, np.uint8)
        for rect in rectList:
            cx, cy = rect.posCenter
            w, h = rect.size
            cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
            cvzone.cornerRect(imgNew, (cx-w//2, cy-h//2, w, h), 20, rt = 0)

        out = img.copy()
        alpha = 0.1 # 透明度
        mask = imgNew.astype(bool)
        out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

        cv2.imshow("img", out)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()