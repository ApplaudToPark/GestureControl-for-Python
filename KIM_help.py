import cv2
import HandTrackingModule as htm
import numpy as np
import time
import math

# trigger의 손모양인지 아닌지를 판별하는 함수. 함수가 많아지면 HandTrackingModule에 모두 넣을 예정.
def classify_trigger(w, h, xlist_tot, ylist_tot, count_time) : # if문을 안으로 넣을 것인지 판단 필요.
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance59 = math.hypot((xlist_tot[5] - xlist_tot[9]) * w_scale, (ylist_tot[5] - ylist_tot[9]) * h_scale)
    distance913 = math.hypot((xlist_tot[13] - xlist_tot[9]) * w_scale, (ylist_tot[13] - ylist_tot[9]) * h_scale)
    distance1317 = math.hypot((xlist_tot[17] - xlist_tot[13]) * w_scale, (ylist_tot[17] - ylist_tot[13]) * h_scale)

    if (distance59 > 60) & (distance913 > 60) & (distance1317 > 55) :
        if (ylist_tot[8] < ylist_tot[6]) & (ylist_tot[12] < ylist_tot[10]) & (ylist_tot[16] < ylist_tot[14]) & (ylist_tot[20] < ylist_tot[18]) :
            print('trigger....')
            # print(distance59)
            # print(ylist_tot[8], ylist_tot[6])
            # print(ylist_tot[12], ylist_tot[10])
            # print(ylist_tot[16], ylist_tot[14])
            # print(ylist_tot[20], ylist_tot[18])
            # print(xlist_tot)
            print(3-int(count_time), 'sec(s) left.')
            return 1
        else :
            print('not trigger1')
            return -1
    else :
        print('not trigger2')
        print(distance59, distance913, distance1317)
        return -1



def left_side(w, h, xlist_tot, ylist_tot) :
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance58 = math.hypot((xlist_tot[5] - xlist_tot[8]) * w_scale, (ylist_tot[5] - ylist_tot[8]) * h_scale)
    distance812 = math.hypot((xlist_tot[8] - xlist_tot[12]) * w_scale, (ylist_tot[8] - ylist_tot[12]) * h_scale)
    distance1216 = math.hypot((xlist_tot[12] - xlist_tot[16]) * w_scale, (ylist_tot[12] - ylist_tot[16]) * h_scale)
    # print("58:", distance58)
    # print("812:", distance812)
    # print("1216:", distance1216)
    # print(xlist_tot[5], xlist_tot[8])
    if (distance58 > 200) & (distance812 < 120) & (distance1216 > 240) & (xlist_tot[8] > xlist_tot[5] + 50) :
        print('left')



def right_side(w, h, xlist_tot, ylist_tot) :
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance58 = math.hypot((xlist_tot[5] - xlist_tot[8]) * w_scale, (ylist_tot[5] - ylist_tot[8]) * h_scale)
    distance812 = math.hypot((xlist_tot[8] - xlist_tot[12]) * w_scale, (ylist_tot[8] - ylist_tot[12]) * h_scale)
    distance1216 = math.hypot((xlist_tot[12] - xlist_tot[16]) * w_scale, (ylist_tot[12] - ylist_tot[16]) * h_scale)
    # print("58:", distance58)
    # print("812:", distance812)
    # print("1216:", distance1216)
    # print(xlist_tot[5], xlist_tot[8])
    if (distance58 > 200) & (distance812 < 120) & (distance1216 > 240) & (xlist_tot[5] > xlist_tot[8] + 40) :
        print('right')



def upper_side(w, h, xlist_tot, ylist_tot) :
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance58 = math.hypot((xlist_tot[5] - xlist_tot[8]) * w_scale, (ylist_tot[5] - ylist_tot[8]) * h_scale)
    distance812 = math.hypot((xlist_tot[8] - xlist_tot[12]) * w_scale, (ylist_tot[8] - ylist_tot[12]) * h_scale)
    distance1216 = math.hypot((xlist_tot[12] - xlist_tot[16]) * w_scale, (ylist_tot[12] - ylist_tot[16]) * h_scale)
    # print("58:", distance58)
    # print("812:", distance812)
    # print("1216:", distance1216)
    # print(ylist_tot[5], ylist_tot[8])
    if (distance58 > 140) & (distance812 < 300) & (distance1216 > 270) & (ylist_tot[5] > ylist_tot[8] + 50) :
        print('upper')



def lower_side(w, h, xlist_tot, ylist_tot) :
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance58 = math.hypot((xlist_tot[5] - xlist_tot[8]) * w_scale, (ylist_tot[5] - ylist_tot[8]) * h_scale)
    distance812 = math.hypot((xlist_tot[8] - xlist_tot[12]) * w_scale, (ylist_tot[8] - ylist_tot[12]) * h_scale)
    distance1216 = math.hypot((xlist_tot[12] - xlist_tot[16]) * w_scale, (ylist_tot[12] - ylist_tot[16]) * h_scale)
    # print("58:", distance58)
    # print("812:", distance812)
    # print("1216:", distance1216)
    # print(ylist_tot[5], ylist_tot[8])
    if (distance58 > 140) & (distance812 < 300) & (distance1216 > 270) & (ylist_tot[8] > ylist_tot[5] + 50) :
        print('lower')



wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# not-activated assigns 0
status_crop = 0
status_trigger = 0

count_time = 0

#######################
x_fixed = 0
y_fixed = 0
w_fixed = 0
h_fixed = 0
cTime = 0
pTime = -1
distance = []
xlist_tot = []
ylist_tot = []
#######################


detector = htm.handDetector(maxHands=1, detectionCon=0.7)

while True :
    success, img = cap.read()
    img = detector.findHands(img)

    try :
        lmList = detector.findPosition(img, draw=False)

    except :
        status_crop = 0
        status_trigger = 0
        x_fixed, y_fixed = 0, 0
        w_fixed, h_fixed = 0, 0
        cTime = 0
        pTime = -1

    else :
        xlist = []
        ylist = []
        xlist_tot = []
        ylist_tot = []

        for i in range(len(lmList[0])) :
            xlist_tot.append(lmList[0][i][1])
            ylist_tot.append(lmList[0][i][2])

        for i in range(6) :
            xlist.append(lmList[0][4*i][1])
            ylist.append(lmList[0][4*i][2])

        xmin = int(min(xlist))
        ymin = int(min(ylist))
        xmax = int(max(xlist))
        ymax = int(max(ylist))

        x, y = xmin, ymin
        w, h = (xmax-xmin), (ymax-ymin)

        if status_trigger == 0 :
            if (x-w//5 > 0) & (y-h//5 > 0) :
                if (x + 6 * w // 5 < wCam) & (y + 6 * h // 5 < hCam) : # classify_trigger에 넣을지 말지 결정해야함.
                    if classify_trigger(w, h, xlist_tot, ylist_tot, count_time) == 1 :
                        w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
                        w_scale, h_scale = wCam / w1, hCam / h1

                    # xbar12, ybar12 = (xlist_tot[4] + xlist_tot[8]) // 2, (ylist_tot[4] + ylist_tot[8]) // 2
                    # xbar23, ybar23 = (xlist_tot[8] + xlist_tot[12]) // 2, (ylist_tot[8] + ylist_tot[12]) // 2
                    # xbar34, ybar34 = (xlist_tot[12] + xlist_tot[16]) // 2, (ylist_tot[12] + ylist_tot[16]) // 2

                    # print(distance12, distance23, distance34)


                    # cv2.line(img, (x4, y4), (x8, y8), (255, 0, 255), 3)
                    # cv2.circle(img, (xbar12, ybar12), 10, (255, 0, 255), cv2.FILLED)
                    # cv2.line(img, (x8, y8), (x12, y12), (255, 0, 255), 3)
                    # cv2.circle(img, (xbar23, ybar23), 10, (255, 0, 255), cv2.FILLED)
                    # cv2.line(img, (x12, y12), (x16, y16), (255, 0, 255), 3)
                    # cv2.circle(img, (xbar34, ybar34), 10, (255, 0, 255), cv2.FILLED)
                    # cv2.line(img, (x16, y16), (x20, y20), (255, 0, 255), 3)
                    # cv2.circle(img, (xbar45, ybar45), 10, (255, 0, 255), cv2.FILLED)

                    # cv2.putText(img, f'dis = {int(distance12)}', (xbar12, ybar12),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0))
                    # cv2.putText(img, f'dis = {int(distance23)}', (xbar23, ybar23),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0))
                    # cv2.putText(img, f'dis = {int(distance12)}', (xbar34, ybar34),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0))
                    # cv2.putText(img, f'dis = {int(distance12)}', (xbar45, ybar45),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0))


                        if pTime == -1 : # time모듈에서 time함수는 음의 값이 나올 수 없으므로.
                            cTime = time.time()
                            pTime = cTime
                        else : cTime = time.time()

                        cropped_img = img[y-h//5 : y+6*h//5, x-w//5 : x+6*w//5]
                        # cv2.putText(img, f'flatten your hands in {3-int(count_time)} sec(s).', (x-w//5, y),
                        #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

                        count_time = count_time + cTime - pTime  # 3초가 흘렀다는 것을 어떻게 표현할 수 있는지? if문을 만듦.

                        status_crop = 1

                        if (3-count_time) < 0 :
                            status_trigger = 1
                            count_time = 0

                            x_fixed, y_fixed = x, y
                            w_fixed, h_fixed = w, h
                            sized_fixed_img = img[y_fixed-h_fixed//5 : y_fixed+6*h_fixed//5, x_fixed-w_fixed//5 : x_fixed+6*w_fixed//5]

                    else :
                        status_crop = 0
                        status_trigger = 0
                        x_fixed, y_fixed = 0, 0
                        w_fixed, h_fixed = 0, 0
                        cTime = 0
                        pTime = -1
                        count_time = 0


                else :
                    status_crop = 0
                    status_trigger = 0
                    x_fixed, y_fixed = 0, 0
                    w_fixed, h_fixed = 0, 0
                    cTime = 0
                    pTime = -1
                    count_time = 0
            else :
                status_crop = 0
                status_trigger = 0
                x_fixed, y_fixed = 0, 0
                w_fixed, h_fixed = 0, 0
                cTime = 0
                pTime = -1
                count_time = 0

        else : # status_trigger = 1이 된 후, 동작하는 코드.
            sized_fixed_img = img[y_fixed-h_fixed//5 : y_fixed+6*h_fixed//5, x_fixed-w_fixed//5 : x_fixed+6*w_fixed//5]





    if status_crop == 1 :
        if status_trigger == 1 : # trigger가 인식된 경우
            resized_img = cv2.resize(sized_fixed_img, (wCam, hCam))
            cv2.imshow("Img", resized_img)

            left_side(w, h, xlist_tot, ylist_tot)
            right_side(w, h, xlist_tot, ylist_tot)
            upper_side(w, h, xlist_tot, ylist_tot)
            lower_side(w, h, xlist_tot, ylist_tot)


        else :
            resized_img = cv2.resize(cropped_img, (wCam, hCam))
            cv2.imshow("Img", resized_img)
            pTime = cTime



    else : # crop을 안하는 상황인 경우
        cv2.imshow("Img", img)


    cv2.waitKey(1)

