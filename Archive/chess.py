from lisbonpose.transform import four_point_transform
import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import cv2
today = date.today()
date = today.strftime("%d/%m/%Y")

def getFirstFrame(videofile):
    vidcap = cv2.VideoCapture(videofile)
    success, image = vidcap.read()
    if success:
        return image

vidpath = '../../Data/lisbon_data/PA02LAC11.mp4'
image = getFirstFrame(vidpath)
#image = image[800:1080, 900:1420]
image = cv2.resize(image, (0,0), fx=0.8, fy=0.8) 

output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret, thresh = cv2.threshold(gray, 100, 150, cv2.THRESH_BINARY)

ret, corners = cv2.findChessboardCorners(thresh, (9,6), None)

'''
output = cv2.drawChessboardCorners(output, (9,6), corners, True)
cv2.imshow('img', output)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite(f'output/chessboard{date}.png', output)

edges = image.copy()
for i in [0, 8, 45, 53]:
	x, y = corners[i][0]
	cv2.circle(edges, (x, y), 2, (0, 0, 255), 5)
	cv2.imshow('edges', edges)
	cv2.waitKey()
	cv2.destroyAllWindows()
'''

top_left 	 = corners[ 0][0]
top_right 	 = corners[ 8][0]
bottom_left  = corners[45][0]
bottom_right = corners[53][0]

pts = np.array([
	top_left,
	bottom_left,
	bottom_right,
	top_right
	], dtype = 'int32')

square = image.copy()
cv2.polylines(square, np.int32([pts]), 1, (0,0,255), 4)
cv2.imshow('square', square)
cv2.waitKey()


warped_cropped, tfm = four_point_transform(image, 
	pts.reshape(4, 2)) # HOW IS GORUND CROPPED AND EXTRACT TFM FROM HERE

warped = cv2.warpPerspective(square, tfm, (8000, 6000)) #This bit crops around rectangle
warped = cv2.resize(warped, (0,0), fx=0.1, fy=0.1) 


cv2.imshow('warped_cropped', warped)
cv2.waitKey()
cv2.destroyAllWindows()