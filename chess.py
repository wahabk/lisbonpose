import numpy as np
import cv2
import matplotlib.pyplot as plt

from checkerboard import detect_checkerboard


def getFirstFrame(videofile):
    vidcap = cv2.VideoCapture(videofile)
    success, image = vidcap.read()
    if success:
        return image

size = (9, 6) # size of checkerboard
#vidpath = '/home/wahab/Downloads/checkerboard_check_vid_example.mp4'
#image = getFirstFrame(vidpath)
image = cv2.imread('Photos/1.jpg')
#image = image[800:980, 500:800]
image = cv2.resize(image, (0,0), fx=1/2, fy=1/2) 
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret, thresh = cv2.threshold(gray, 100, 170, cv2.THRESH_BINARY)

cv2.imshow('img', thresh)
cv2.waitKey()
cv2.destroyAllWindows()

ret, corners = detect_checkerboard(thresh, size, None)

image = cv2.drawChessboardCorners(image, (2,4), corners, True)
#plt.scatter('img', image, extent=corners[0]), plt.show()

cv2.imshow('img', image)
cv2.waitKey()
cv2.destroyAllWindows()