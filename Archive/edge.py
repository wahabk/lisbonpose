from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import matplotlib.pyplot as plt
import numpy as np
import argparse
import imutils
import cv2

def cropFloor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('/home/wahab/Data/template.jpg', 0)
    template = template.astype(np.uint8)

    x, y = template.shape[::-1]

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + x, top_left[1] + y)
    
    cv2.rectangle(gray, top_left, bottom_right, 255, 2)
    cropped = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return cropped

def slope(point1, point2):
	m = (point2[1] - point1[1])/(point2[0] - point1[0])
	return m

def getC(point, m):
	c =  point[1] - (m * point[0])
	return c

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]


img = cv2.imread('../Data/control1frame1.jpg')
img = cropFloor(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = gray.astype('uint8')

blurred = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)[1]
edged = cv2.Canny(thresh, 2, 2)

'''
plt.subplot(121)
plt.imshow(img, cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(122)
plt.imshow(thresh, cmap = 'gray')
plt.title('threshold'), plt.xticks([]), plt.yticks([])
plt.show()
plt.subplot(121)
plt.imshow(img, cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(122)
plt.imshow(edged, cmap = 'gray')
plt.title('Edgy'), plt.xticks([]), plt.yticks([])
plt.show()
'''

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

# show the contour (outline) of the piece of paper
img2 = img.copy()
cv2.drawContours(img2, [screenCnt], -1, (0, 255, 0), 2)

plt.subplot()
plt.imshow(img2, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])
plt.show()


#Make into a rectangle
#Create line paralell to the top line but draw it on bottom of contour

top_left = 		screenCnt[0][0]
bottom_left = 	screenCnt[1][0]
bottom_right =  screenCnt[2][0]
top_right = 	screenCnt[3][0]
new_line_left = (bottom_left[0] - 10, bottom_left[1] - 10)

m = slope(top_left, top_right)
c = getC(new_line_left, m)
if m == 0:
	print("ERROR: M IS ZERO!!!!!!!!")

new_line_right_y = 	(m * (bottom_right[0] + 20)) + c
new_line_right_x = 	(new_line_right_y - c) / m
new_line_right = 	(int(new_line_right_x), int(new_line_right_y))
new_line = 			(new_line_left, new_line_right)

#Draw new bottom line
cv2.line(img2, new_line_left, new_line_right, (255,0,0), 2)

plt.subplot()
plt.imshow(img2, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])
plt.show()

#Find intersects and set as new bottom corners or rectangle
left_line = 		(top_left, bottom_left)
right_line = 		(top_right, bottom_right)
new_bottom_left = 	line_intersection(new_line, left_line)
new_bottom_right = 	line_intersection(new_line, right_line)

#Reassign new contour box
new_screenCnt = np.array([	[top_left],
					[new_bottom_left],
					[new_bottom_right],
					[top_right]], dtype = 'int')

img3 = img.copy()
cv2.drawContours(img3, [new_screenCnt], -1, (255, 0, 0), 2)
plt.subplot()
plt.imshow(img3, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])
plt.show()

#Crop and warp image
warped = four_point_transform(img3, new_screenCnt.reshape(4, 2))
plt.subplot()
plt.imshow(warped, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])
plt.show()