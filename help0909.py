import cv2
import HandTrackingModule as htm
import numpy as np
import time
import math

# trigger의 손모양인지 아닌지를 판별하는 함수. 함수가 많아지면 HandTrackingModule에 모두 넣을 예정.
def classify_trigger(w, h, xlist_tot, ylist_tot) : # if문을 안으로 넣을 것인지 판단 필요.
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance59 = math.hypot((xlist_tot[5] - xlist_tot[9]) * w_scale, (ylist_tot[5] - ylist_tot[9]) * h_scale)
    distance913 = math.hypot((xlist_tot[13] - xlist_tot[9]) * w_scale, (ylist_tot[13] - ylist_tot[9]) * h_scale)
    distance1317 = math.hypot((xlist_tot[17] - xlist_tot[13]) * w_scale, (ylist_tot[17] - ylist_tot[13]) * h_scale)

    if (distance59 > 60) & (distance913 > 60) & (distance1317 > 55) :
        if (ylist_tot[8] < ylist_tot[6]) & (ylist_tot[12] < ylist_tot[10]) & (ylist_tot[16] < ylist_tot[14]) & (ylist_tot[20] < ylist_tot[18]) & (ylist_tot[4]<ylist_tot[0]) :
            return 1
        else :
            print("none1")
            return -1
    else :
        print("none2")
        return -1


# trigger이후 관절과의 위치관계를 파악하여 새로운 함수를 불러오는 역할을 함. 액자식 구성의 함수
def operate_func(w_scale, h_scale, xlist_tot, ylist_tot) :
    k1 = w_scale
    k2 = h_scale

    distance812 = math.hypot(w_scale*(xlist_tot[8]-xlist_tot[12]), h_scale*(ylist_tot[8]-ylist_tot[12]))
    distance1216 = math.hypot(w_scale * (xlist_tot[12] - xlist_tot[16]), h_scale * (ylist_tot[12] - ylist_tot[16]))
    # print("검지-중지", w_scale*(xlist_tot[8]-xlist_tot[12]))
    # print("중지-약지", w_scale*(xlist_tot[12]-xlist_tot[16]))
    # print("y:중지-약지", h_scale*(ylist_tot[16]-ylist_tot[12]))
    # print()


    if distance812 < 100 :
        if distance1216 < 200 : # 세 손가락이 붙어있는 경우
            pass
            # print("세 손가락", distance812, distance1216)


        else : # 두 손가락만 붙어있는 경우
            # print("두 손가락", distance812, distance1216)
            return two_fingers(k1, k2, xlist_tot, ylist_tot)

    else :
        pass
        # print("이도저도 아님", distance812, distance1216)

# 두 손가락에 관한 동작을 담은 함수
def two_fingers(w_scale, h_scale, xlist_tot, ylist_tot) :
    bound_x = 120
    bound_y = 80
    standard_x = (xlist_tot[5] + xlist_tot[9])//2
    standard_y = (ylist_tot[5] + ylist_tot[9])//2

    position812_x = (xlist_tot[8] + xlist_tot[12])//2
    position812_y = (ylist_tot[8] + ylist_tot[12])//2

    x = w_scale * (position812_x-standard_x)
    y = h_scale * (position812_y-standard_y)

    # 임시적으로 라인 표시하기
    cv2.circle(img, (standard_x-bound_x, standard_y-bound_y), 5, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (standard_x+bound_x, standard_y-bound_y), 5, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (standard_x-bound_x, standard_y+bound_y), 5, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (standard_x+bound_x, standard_y+bound_y), 5, (255, 0, 255), cv2.FILLED)
    cv2.line(img, (standard_x-bound_x, standard_y-bound_y), (standard_x+bound_x, standard_y-bound_y), (255, 0, 255), 3)
    cv2.line(img, (standard_x-bound_x, standard_y+bound_y), (standard_x+bound_x, standard_y+bound_y), (255, 0, 255), 3)
    cv2.line(img, (standard_x-bound_x, standard_y-bound_y), (standard_x-bound_x, standard_y+bound_y), (255, 0, 255), 3)
    cv2.line(img, (standard_x+bound_x, standard_y-bound_y), (standard_x+bound_x, standard_y+bound_y), (255, 0, 255), 3)

    # print("standards", standard_x, standard_y)
    # print("two fingers", position812_x, position812_y)
    # print(x, y)


    if (x < -bound_x) & (y > -bound_y) & (y < bound_y) :
        print("left")
        return "two_fingers", (-1, 0)

    elif (x > bound_x) & (y > -bound_y) & (y < bound_y) :
        print("right")
        return "two_fingers", (1, 0)

    elif (y < -bound_y) & (x > -bound_x) & (x < bound_x) :
        print("up")
        return "two_fingers", (0, 1)

    elif (y > bound_y) & (x > -bound_x) & (x < bound_x) :
        print("down")
        return "two_fingers", (0, -1)

    elif (x < -bound_x) & (y < -bound_y) :
        print("up-left")
        return "two_fingers", (-1, 1)

    elif (x > bound_x) & (y < -bound_y) :
        print("up-right")
        return "two_fingers", (1, 1)

    elif (x < -bound_x) & (y > bound_y) :
        print("down-left")
        return "two_fingers", (-1, -1)

    elif (x > bound_x) & (y > bound_y) :
        print("down-right")
        return "two_fingers", (1,-1)

    else :
        print("none")
        print(x, y, bound_x, bound_y)



wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# not-activated assigns 0
status_crop = 0
status_trigger = 0

count_time = 0
NonDetectionTime = 0

#######################
x_fixed = 0
y_fixed = 0
w_fixed = 0
h_fixed = 0
cTime = 0
pTime = -1
lTime = 0
kTime = -1
distance = []
#######################


detector = htm.handDetector(maxHands=1, detectionCon=0.7)

while True :
    success, img = cap.read()
    img = detector.findHands(img)

    try :
        lTime = time.time()
        lmList = detector.findPosition(img, draw=False)

    except : # 손 인식을 하지 못하여 trigger가 풀리는 현상을 방지하기 위한 코드
        if status_trigger == 1 :
            if kTime == -1 :
                kTime = lTime

            else :
                NonDetectionTime = lTime - kTime + NonDetectionTime
                kTime = lTime

                if NonDetectionTime > 3 :
                    status_trigger = 0
                    status_crop = 0
                    NonDetectionTime = 0
                else : pass

        else :
            status_crop = 0
            x_fixed, y_fixed = 0, 0
            w_fixed, h_fixed = 0, 0
            cTime = 0
            pTime = -1



    else :
        NonDetectionTime = 0
        lTime = 0
        kTime = -1
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
                    if classify_trigger(w, h, xlist_tot, ylist_tot) == 1 :
                        w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
                        w_scale, h_scale = wCam / w1, hCam / h1

                        if pTime == -1 : # time모듈에서 time함수는 음의 값이 나올 수 없으므로.
                            cTime = time.time()
                            pTime = cTime
                        else : cTime = time.time()

                        cropped_img = img[y-h//5 : y+6*h//5, x-w//5 : x+6*w//5]

                        count_time = count_time + cTime - pTime  # 3초가 흘렀다는 것을 어떻게 표현할 수 있는지? if문을 만듦.

                        status_crop = 1

                        if (3-count_time) < 0 :
                            status_trigger = 1
                            count_time = 0

                            x_fixed, y_fixed = x, y
                            w_fixed, h_fixed = w, h


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
            operate_func(w_scale, h_scale, xlist_tot, ylist_tot)




    if status_crop == 1 :
        if status_trigger == 1 : # trigger가 인식된 경우
            cv2.imshow("Img", img)

        else :
            resized_img = cv2.resize(cropped_img, (wCam, hCam))
            cv2.imshow("Img", resized_img)
            pTime = cTime



    else : # crop을 안하는 상황인 경우
        cv2.imshow("Img", img)


    cv2.waitKey(1)

