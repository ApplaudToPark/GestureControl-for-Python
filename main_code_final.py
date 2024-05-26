import cv2
import HandTrackingModule as htm
import numpy as np
import time
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

# trigger의 손모양인지 아닌지를 판별하는 함수. 함수가 많아지면 HandTrackingModule에 모두 넣을 예정.
def classify_trigger(w, h, xlist_tot, ylist_tot) : # if문을 안으로 넣을 것인지 판단 필요.
    w1, h1 = 6 * w // 5 + w // 5, 6 * h // 5 + h // 5
    w_scale, h_scale = wCam / w1, hCam / h1
    distance59 = math.hypot((xlist_tot[5] - xlist_tot[9]) * w_scale, (ylist_tot[5] - ylist_tot[9]) * h_scale)
    distance913 = math.hypot((xlist_tot[13] - xlist_tot[9]) * w_scale, (ylist_tot[13] - ylist_tot[9]) * h_scale)
    distance1317 = math.hypot((xlist_tot[17] - xlist_tot[13]) * w_scale, (ylist_tot[17] - ylist_tot[13]) * h_scale)

    if (distance59 > 60) & (distance913 > 60) & (distance1317 > 55) & (ylist_tot[4] > ylist_tot[8]) :
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

    distance58 = math.hypot(w_scale*(xlist_tot[5]-xlist_tot[8]), h_scale*(ylist_tot[5]-ylist_tot[8]))
    distance48 = math.hypot(w_scale*(xlist_tot[4]-xlist_tot[8]), h_scale*(ylist_tot[4]-ylist_tot[8]))
    distance812 = math.hypot(w_scale*(xlist_tot[8]-xlist_tot[12]), h_scale*(ylist_tot[8]-ylist_tot[12]))
    distance1216 = math.hypot(w_scale * (xlist_tot[12] - xlist_tot[16]), h_scale * (ylist_tot[12] - ylist_tot[16]))
    distance1620 = math.hypot(w_scale * (xlist_tot[20] - xlist_tot[16]), h_scale * (ylist_tot[20] - ylist_tot[16]))
    # print("검지-중지", w_scale*(xlist_tot[8]-xlist_tot[12]))
    # print("중지-약지", w_scale*(xlist_tot[12]-xlist_tot[16]))
    # print("y:중지-약지", h_scale*(ylist_tot[16]-ylist_tot[12]))
    # print()


    if (ylist_tot[5] > ylist_tot[8]) :
        if (ylist_tot[12] > ylist_tot[9]) & (ylist_tot[16] > ylist_tot[13]) & (ylist_tot[4] < ylist_tot[12]) :
            return point_finger(k1, k2, xlist_tot, ylist_tot)

        elif (ylist_tot[12] < ylist_tot[9]) & (ylist_tot[16] > ylist_tot[13]) :
            return two_fingers(k1, k2, xlist_tot, ylist_tot)

        # elif (ylist_tot[12] < ylist_tot[9]) & (ylist_tot[16] < ylist_tot[13]) & (ylist_tot[20] < ylist_tot[17]) & (ylist_tot[4] > ylist_tot[5]) :
        #     return turn_off()

    elif (ylist_tot[8] > ylist_tot[5]) & (ylist_tot[12] > ylist_tot[9]) & (ylist_tot[16] > ylist_tot[13]) :
        return mandoo(k1, k2, xlist_tot, ylist_tot)



# 두 손가락에 관한 동작을 담은 함수
def two_fingers(w_scale, h_scale, xlist_tot, ylist_tot) :
    global plocX
    global plocY
    global clocX
    global clocY
    global x_old1
    global y_old1

    plocX, plocY, clocX, clocY = -1, -1, 0, 0
    x_old1, y_old1 = -1, -1

    bound_x = 120 // w_scale
    bound_y = 80 // h_scale
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
        pyautogui.press("left")
        time.sleep(0.5)
        return "two_fingers", (-1, 0)

    elif (x > bound_x) & (y > -bound_y) & (y < bound_y) :
        pyautogui.press("right")
        time.sleep(0.4)
        return "two_fingers", (1, 0)

    elif (y < -bound_y) & (x > -bound_x) & (x < bound_x) :
        pyautogui.press("up")
        # time.sleep(1)
        return "two_fingers", (0, 1)

    elif (y > bound_y) & (x > -bound_x) & (x < bound_x) :
        pyautogui.press("down")
        time.sleep(0.4)
        return "two_fingers", (0, -1)

    elif (x < -bound_x) & (y < -bound_y) :
        pyautogui.press("up")
        pyautogui.press("left")
        time.sleep(0.4)
        return "two_fingers", (-1, 1)

    elif (x > bound_x) & (y < -bound_y) :
        pyautogui.press("up")
        pyautogui.press("right")
        time.sleep(0.4)
        return "two_fingers", (1, 1)

    elif (x < -bound_x) & (y > bound_y) :
        pyautogui.press("down")
        pyautogui.press("left")
        time.sleep(0.4)
        return "two_fingers", (-1, -1)

    elif (x > bound_x) & (y > bound_y) :
        pyautogui.press("down")
        pyautogui.press("right")
        time.sleep(0.4)
        return "two_fingers", (1,-1)

    else :
        print("none")
        print(x, y, bound_x, bound_y)


# 검지 손가락을 핀 경우, x와 y는 operate function에서 받을 예정.
def point_finger(w_scale, h_scale, xlist_tot, ylist_tot) :
    global x_old1
    global y_old1
    global clocX
    global clocY
    global plocX
    global plocY
    global status_func

    x_old1, y_old1 = -1, -1

    width, height = pyautogui.size()
    x1, y1 = xlist_tot[8], ylist_tot[8]
    x2 = np.interp(x1, (0, wCam), (0, width))
    y2 = np.interp(y1, (0, hCam), (0, height))

    # if status_func != "point_finger" :
    #     x_old = -1
    #     y_old = -1

    distance410 = math.hypot(w_scale * (xlist_tot[4] - xlist_tot[10]), h_scale * (ylist_tot[4] - ylist_tot[10]))

    coor1 = xlist_tot[4], ylist_tot[4]
    coor2 = xlist_tot[10], ylist_tot[10]
    cv2.line(img, coor1, coor2, (255, 0, 255), 3)

    # if (x_old == -1) or (y_old == -1) :
    #     x_old = xlist_tot[8]
    #     y_old = ylist_tot[8]

    # else :

    if distance410 < 80 : # click 동작
        # time.sleep(0.3)
        if distance410 < 80 :
            cursor = pyautogui.position()
            pyautogui.click(cursor[0], cursor[1])

        else :
            cursor = pyautogui.position()
            pyautogui.click(cursor[0], cursor[1])

    if plocX == -1 :
        cursor = pyautogui.position()
        plocX, plocY = cursor[0], cursor[1]

    clocX = plocX + (x2-plocX)/smooth_scale
    clocY = plocY + (y2-plocY)/smooth_scale

    # cursor 이동
    try :
        cursor = pyautogui.position()
        # pyautogui.moveTo((del_x * w_scale * 3 + cursor[0], del_y * h_scale * 3 + cursor[1]))
        pyautogui.moveTo((width-clocX, clocY))
    except :
        pass

    else :
        plocX = clocX
        plocY = clocY

    return "point_finger"


def mandoo(w_scale, h_scale, xlist_tot, ylist_tot) :
    global x_old1
    global y_old1
    global status_func
    global plocX
    global plocY
    global clocX
    global clocY

    plocX, plocY, clocX, clocY = 0, 0, 0, 0

    volRange = volume.GetVolumeRange()  # tuple 형태로 반환

    # x_new = (xlist_tot[4] + xlist_tot[8] + xlist_tot[12])//3
    y_new = (ylist_tot[8] + ylist_tot[12] + ylist_tot[16] + ylist_tot[20] + ylist_tot[0])//5

    # if status_func != "mandoo" :
    #     print(status_func)
    #     x_old = -1
    #     y_old = -1


    if y_old1 == -1 :
        # x_old = (xlist_tot[4] + xlist_tot[8] + xlist_tot[12])//3
        y_old1 = (ylist_tot[8] + ylist_tot[12] + ylist_tot[16] + ylist_tot[20] + ylist_tot[0])//5

    cv2.circle(img, (330, y_old1), 5, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (330, y_new), 5, (0, 255, 0), cv2.FILLED)
    length = y_old1 - y_new
    distance46 = math.hypot(w_scale * (xlist_tot[4] - xlist_tot[6]), h_scale * (ylist_tot[4] - ylist_tot[6]))

    if (distance46 < 60) :
        volume.SetMasterVolumeLevel(volRange[0], None)
        time.sleep(1)
    else :
        vol = np.interp(length, [-50, 150], [volRange[0], volRange[1]])
        volume.SetMasterVolumeLevel(vol, None)

    return "mandoo", "mandoo"


# def turn_off() :
#     global turn
#     if turn == 1 :
#         # 화면을 끄는 함수(cec)
#
#     else :
#         pass



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
cTime = 0
pTime = -1
lTime = 0
kTime = -1
distance = []
x_old, y_old = -1, -1
x_old1, y_old1 = -1, -1
status_func = ""
smooth_scale = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0
turn = 0
#######################


detector = htm.handDetector(maxHands=1, detectionCon=0.7)

####################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume.SetMasterVolumeLevel(0, None)
################


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

                if NonDetectionTime > 2 :
                    status_trigger = 0
                    status_crop = 0
                    status_func = ""
                    plocX, plocY = 0, 0
                    clocX, clocY = 0, 0
                    # x_old1, y_old1 = -1, -1
                    NonDetectionTime = 0
                else : pass

        else :
            status_crop = 0
            cTime = 0
            pTime = -1
            plocX, plocY = 0, 0
            clocX, clocY = 0, 0
            x_old1, y_old1 = -1, -1
            status_func = ""


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


                    else :
                        status_crop = 0
                        status_trigger = 0
                        cTime = 0
                        pTime = -1
                        count_time = 0
                        plocX, plocY = 0, 0
                        clocX, clocY = 0, 0
                        x_old1, y_old1 = -1, -1
                        status_func = ""

                else :
                    status_crop = 0
                    status_trigger = 0
                    cTime = 0
                    pTime = -1
                    count_time = 0
                    plocX, plocY = 0, 0
                    clocX, clocY = 0, 0
                    x_old1, y_old1 = -1, -1
                    status_func = ""

            else :
                status_crop = 0
                status_trigger = 0
                cTime = 0
                pTime = -1
                count_time = 0
                plocX, plocY = 0, 0
                clocX, clocY = 0, 0
                x_old1, y_old1 = -1, -1
                status_func = ""

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

