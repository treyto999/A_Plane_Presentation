# Server application. Receives data from meanShift and classifies it
from socket import *
import cv2 as cv
import multiprocessing as mp
import sys
import time
import pyautogui
import numpy as np

def digest(buffer1, buffer2):
    MOVE_CONST = 40
    FUZZY_CONST = 1000

    xMean1 = np.mean(buffer1[0])
    yMean1 = np.mean(buffer1[1])
    xMean2 = np.mean(buffer2[0])
    yMean2 = np.mean(buffer2[1])

    xDirection = ""
    yDirection = ""

    xMoveDir = (xMean1 - xMean2)
    yMoveDir = (yMean1 - yMean2)

    if xMoveDir > MOVE_CONST:
        if xMoveDir < FUZZY_CONST:
            xDirection = "left"

    if xMoveDir < -MOVE_CONST:
        if xMoveDir > -FUZZY_CONST:
            xDirection = "right"

    if yMoveDir > MOVE_CONST:
        if yMoveDir < FUZZY_CONST:
            yDirection = "down"

    if yMoveDir < -MOVE_CONST:
        if yMoveDir > -FUZZY_CONST:
            yDirection = "up"

    return xDirection, yDirection



if __name__ == '__main__' :

    THRESHOLD = 5

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 12000))

    buffer1 = []
    buffer2 = []

    print ("The server is now ready to receive packets")
    while True:

        message, address = serverSocket.recvfrom(8)

        vals = message.decode().split()
        if message.decode() == "end":
            break

        if len(buffer1) < THRESHOLD:
            buffer1.append( [int(vals[0]) , int(vals[1])] )
        elif len(buffer2) < THRESHOLD:
            buffer2.append( [int(vals[0]) , int(vals[1])] )
        else:
            xdir, ydir = digest(buffer1, buffer2)
            print([xdir])
            if(xdir == "left"):
                pyautogui.click(x=1670, y=1030)            
            if(xdir == "right"):
                pyautogui.click(x=1730, y=1030)            
            buffer1 = []
            buffer2 = []



