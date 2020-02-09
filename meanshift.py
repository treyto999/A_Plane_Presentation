import numpy as np
import cv2 as cv
import pyautogui
from socket import *
import time

clientSocket = socket(AF_INET, SOCK_DGRAM)
print("The client is ready to send data")
server_address = ("localhost", 12000)

pyautogui.PAUSE = 0

xscalefactor = 1920/640
yscalefactor = 1080/480

cap = cv.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()
frame = cv.flip(frame, +1)

# setup initial location of window
x, y, w, h = 300, 200, 150, 150 # simply hardcoded the values
track_window = (x, y, w, h)

# set up the ROI for tracking
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

counter = 1
while(1):
    time.sleep(0.05)
    ret, frame = cap.read()
    frame = cv.flip(frame, +1)


    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), (255, 255, 255),2)
        cv.imshow('img2',img2)

        message = "" + str(int((x+x+w)/2)) + " " + str(int((y+y+h)/2))
        clientSocket.sendto(message.encode(), server_address)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            clientSocket.sendto("end".encode(), server_address)
            break
    else:
        break
