from tkinter.messagebox import NO
import cv2
from hand_recognize_class import HandDetector
import time


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon = 0.8)
    

    startDist = None
    pTime = 0
    scale = 0  # 设置一个初始的需要缩放的大小

    while True:
        ret, img = cap.read()
        h_cap, w_cap = img.shape[:2]
        hands, img = detector.findHands(img)

        img1 = cv2.imread("./image/horse_temp.jpg")
        img1 = cv2.resize(img1, (100, 100)) # 缩小图像至合适
        h1, w1, _ = img1.shape  # 获取原始图像的宽高

        if len(hands) == 2:
            
            # 检测手指是否朝上的，hands[0]代表第一只手，hands[1]代表第二只手
            # print('which up:', detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
            # 返回值是[1,1,0,0,0]代表一只手中拇指和食指竖起，其他指都没有竖起
            if detector.fingersUp(hands[0]) == [1,1,0,0,0] and detector.fingersUp(hands[1]) == [1,1,0,0,0]:
                
                # 通过两只手食指的关键点之间的距离来缩放图片
                lmList1 = hands[0]['lmList']  # 第一只手的关键点坐标信息，hands是一个字典
                lmList2 = hands[1]['lmList']  # 第二只手的关键点坐标信息
                
                # 第一次检测到食指间的距离
                if startDist is None:
                    
                    # 计算食指间的距离并绘图；食指的关键点索引是8；返回值：连线长度，连线的信息(起点、终点、中点坐标)，绘制后的图像
                    length, info, _  = distance = detector.findDistance(lmList1[8], lmList2[8], img = None)
                    # print('length',length,'info',info)
                    
                    # 检测到的第一帧的食指间的距离作为初始距离，接下来超过这个长度就放大，小于这个长度就缩小
                    startDist = length
                
                # 第一帧检测到距离之后，接下来变动的距离就是用于缩放图片大小
                length, info, _  = distance = detector.findDistance(lmList1[8], lmList2[8], img = None)
                
                # 计算变化量，正数代表放大，负数代表缩小。scale的变化范围过大，除以2使它变化缓慢一些
                scale = (length - startDist) // 2
                
                #（7）按比例缩放图像
                # 获取食指连线的中心点坐标，用于实时改变图像的位置
                cx, cy = info[4:]  # info是一个列表索引4和5存放中心点坐标
                
        # 如果两只手中至少有一只消失了，重置初始距离
        else:
            startDist = None
        
        
        try:  # 用于处理异常，因为一旦缩放的区间变成负数，就会报错
            # 确定需要缩放的图像的宽高
            # 如果scale是奇数，那么计算结果不能被2整除，使得img中的空出的位置的shape和img1的shape不一样
            # newH, newW = h1+scale, w1+scale  
            newH, newW = int(((h1+scale)//2)*2), int(((w1+scale)//2)*2)  
            
            # 改变原图像的shape，先指定宽，后指定高
            img1_ = cv2.resize(img1, (newW, newH))
            
            # 实时改变图像的位置，使图像中心点随着食指间的连线的中点的位置变化
            # 确保newH和newW可以被2整除，不然重组后的img中的shape和img1的shape不同
            img[cx - newH//2:cx + newH//2, w_cap - newW//2:w_cap + newW//2] = img1_  # 先指定高，再指定宽
        
        except: # 否则放在画面正中间
            img[(h_cap - h1)//2:(h_cap + h1)//2, (w_cap - w1)//2:(w_cap + w1)//2] = img1


        # 计算fps
        cTime = time.time()  # 处理每一帧图像所需的时间
        fps = 1/(cTime-pTime)
        pTime = cTime  # 更新处理下一帧图像的起始时间
    
        # 把fps值显示在图像上,img画板,显示字符串,显示的坐标位置,字体,字体大小,颜色,线条粗细
        cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)


        # img = cv2.flip(img, 1) # 镜像操作
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF==27:  #每帧滞留1毫秒后消失，ESC键退出
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()