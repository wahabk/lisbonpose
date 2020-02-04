import cv2
import numpy as np 
import matplotlib.pyplot as plt
import PIL.Image
import PIL.ImageDraw


def getFirstFrame(videofile):
    vidcap = cv2.VideoCapture(videofile)
    success, image = vidcap.read()
    if success:
        return image

vidpath = '/home/wahab/code/Photos/1.jpg'

img = getFirstFrame(vidpath)
img = cv2.resize(img, (0,0), fx=1/2, fy=1/2) 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(gray, 127,170 , cv2.THRESH_BINARY)
cv2.imshow('img', gray)
cv2.waitKey()

ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
x = []
y = []
for i in corners:
	x.append(i[0][0])
	y.append(i[0][1])
maxcorners = np.array([[min(x), min(y)], [min(x), max(y)], [max(x), max(y)], [max(x), min(y)]], np.int32)
print(maxcorners)

#image = cv2.drawChessboardCorners(img, (9,6), corners, ret)

cv2.polylines(img,[maxcorners],True,(0,0,255), 5)

cv2.imshow('img', img)
cv2.waitKey()

'''
Found source points
Define dst points and apply homography
'''