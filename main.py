import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import  cvzone
from pynput.keyboard import Key, Controller

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8, maxHands=2)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ],
        ["^","Z", "X", "C", "V", "B", "N", "M", "x"],
        ['1','_']]
keys_num=[['1','2','3','4','5','6','7','8','9','0'],
          ['-','/',':',';','(',')','#','&','@','"'],
          ['.','?','!','x'],
            ['a','_']

]
keys_lists=[]
keys_list_num=[]
kb=Controller()

class buttons():
    def __init__(self,pos,text,size=[65,65]):
        self.pos = pos
        self.text=text
        self.size = size

def button_draw(img,keys_list):
    imgNew=np.zeros_like(img,np.uint8)
    for button_Value in keys_list:
        x, y = button_Value.pos
        cvzone.cornerRect(imgNew,(button_Value.pos[0],button_Value.pos[1],button_Value.size[0],button_Value.size[1]),20,rt=0)
        cv2.rectangle(imgNew, button_Value.pos, (x+button_Value.size[0],y+button_Value.size[1]), (85, 123, 131), cv2.FILLED)
        cv2.putText(imgNew, button_Value.text, (x + 5, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    out=img.copy()
    alpha=0.5
    mask=imgNew.astype(bool)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out

for x in range(len(keys)):
    for y, key in enumerate(keys[x]):
        keys_lists.append(buttons([100 * y + 50, 100 * x + 50], key))

for x in range(len(keys_num)):
    for y, key in enumerate(keys_num[x]):
        keys_list_num.append(buttons([100 * y + 50, 100 * x + 50], key))

current_key=True
while True:
    success, img =cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    if current_key:
        keys_list=keys_lists
        img = button_draw(img, keys_list)
    else:
        keys_list=keys_list_num
        img=button_draw(img,keys_list_num)
    if hands:
        hand=hands[0]
        lmList=hand['lmList']
        # bbox=hand['bbox']
        if lmList:
            for button in keys_list:
                x,y=button.pos
                w,h=button.size
                if x <lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                    length, _, _ = detector.findDistance([lmList[8][0], lmList[8][1]], [lmList[12][0], lmList[12][1]],img)
                    if length<53:
                        print(length)
                        cv2.rectangle(img, button.pos, (w + x, h + y), (85, 123, 131), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 5, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                        if button.text=="x":
                            kb.press(Key.backspace)
                            kb.release(Key.backspace)
                        elif button.text=='1':
                            current_key=False
                        elif button.text=='a':
                            current_key=True
                        elif button.text=='_':
                            kb.press(Key.space)
                            kb.release(Key.space)
                        else:
                            kb.press(button.text)
                        time.sleep(0.15)





    cv2.imshow("KeyBoard",img)
    key=cv2.waitKey(1)
    if key == 27:
        print('esc is pressed closing all windows')
        cv2.destroyAllWindows()
        break
cap.release()
