from pyimagesearch.transform import four_point_transform
from PIL import Image, ImageDraw
from os.path import isfile, join
import matplotlib.pyplot as plt
from pathlib import Path
from os import listdir
import numpy as np
import argparse
import subprocess
import imutils
import cv2
import math
import json
import os

# Functions ////////////////////////////////////

def read_keypoints(keypoint_filename):
	keypoint_file = keypoint_filename.open()
	keypoint_data = json.load(keypoint_file)
	keypoint_file.close()
	return keypoint_data

def find_pose_keypoints(keypoint_data):
	keypoints = keypoint_data['people']
	if (len(keypoints) >= 1):
		keypoints = keypoints[0] # first person
		keypoints = keypoints['pose_keypoints_2d'] # body points in body25 model
		return keypoints
	else:
		return []

def getFrame(videofile, frame):
    vidcap = cv2.VideoCapture(videofile)

    image = vidcap.get(100)

    success, img = vidcap.read()
    if not success: 
    	raise Exception("Could not load image! :(")
    return img

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
    return cropped, top_left, bottom_right

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
       raise Exception('Lines do not intersect.')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

def calculateDistance(point1, point2):  
     dist = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)  
     return dist

# Start ///////////////////////////////////////////////////////////////////

vid = 				"002_Control_2" #Which video

# DEFINE PATHS


vidpath = 			"/home/wahab/Data/greig_corridor_data/Control/"+vid+".mp4"
directory = 		"Data/Control/"+vid+"/"
directory_json = 	""+directory+"/json/"
pointpath = 		Path(directory_json)
print(vid)

#Make folders
if not os.path.exists(directory): # Create target Directory if don't exist
	os.mkdir(directory)
	os.mkdir(directory_json)
	print("Directory " , directory_json ,  " Created")
	exists = False
else:
	print("Directory " , directory_json ,  " already exists")
	exists = True

#Run openpose and save jsons
if not exists:
	model_folder = '--model_folder ~/deep_learning/openpose/models/'
	p = Popen('~/deep_learning/openpose/build/examples/openpose/openpose.bin '+model_folder+' --video '+vidpath+' --write_json '+directory_json+'', 
			shell=True)
	p.wait()
	p.communicate()

# OPEN FILES
keypoint_files = 	pointpath.iterdir()
img = 				getFrame(vidpath, 5)
img = 				cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

while True:
	
	floor, floor_top_left, floor_bottom_right = cropFloor(img)
	gray = 				cv2.cvtColor(floor, cv2.COLOR_BGR2GRAY).astype('uint8')
	blurred = 			cv2.GaussianBlur(gray, (7, 7), 0) #Blur
	t = int(input('\nthresh value: \n'))
	thresh = 			cv2.threshold(blurred, t, 255, cv2.THRESH_BINARY)[1] #Threshold
	edged = 			cv2.Canny(thresh, 2, 2) #Find edges

	plt.subplot(), plt.imshow(thresh, cmap = 'gray')
	plt.title('Threshold'), plt.xticks([]), plt.yticks([]), plt.show()
exit()

#Find contours around polygons and draw rectangles around, choose the biggest one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
	else:
		raise Exception('Not Enough contours found :( Adjust threshold parameters?')
# show the contour (outline) of the ground
contour = floor.copy()
cv2.drawContours(contour, [screenCnt], -1, (0, 255, 0), 2)

plt.subplot(), plt.imshow(contour, cmap = 'gray')
plt.title('First Contour'), plt.xticks([]), plt.yticks([]), plt.show()






#Define new paralellogram contour
top_left = 			screenCnt[0][0]
bottom_left = 		screenCnt[1][0]
bottom_right =  	screenCnt[2][0]
top_right = 		screenCnt[3][0]
new_line_left = 	(bottom_left[0] - 10, bottom_left[1] - 10) #Adjust new bottom_left above and to the left of previous by 10 pixels
#y = mx + c
m = slope(top_left, top_right)
c = getC(new_line_left, m)
if m == 0:
	raise Exception('ERROR: M IS EQUAL TO ZERO!!!  :(')

#Set new bottom line and draw it
new_line_right_y = 	int((m * (bottom_right[0] + 20)) + c)
new_line_right_x = 	int((new_line_right_y - c) / m)
new_line_right = 	(new_line_right_x, new_line_right_y)
new_bottom_line = 	(new_line_left, new_line_right)

contour2 = contour.copy()
cv2.line(contour2, new_line_left, new_line_right, (255,0,0), 2)

#plt.subplot(), plt.imshow(contour2, cmap = 'gray')
#plt.title('Contour with new bottom line'), plt.xticks([]), plt.yticks([]), plt.show()

#Find intersects of old box against new bottom line and set as new bottom corners of rectangle
left_line = 		(top_left, bottom_left)
right_line = 		(top_right, bottom_right)
new_bottom_left = 	line_intersection(new_bottom_line, left_line)
new_bottom_right = 	line_intersection(new_bottom_line, right_line)

#Reassign new contour box which is a paralellogram and draw it
new_screenCnt = np.array([	[top_left],
							[new_bottom_left],
							[new_bottom_right],
							[top_right]], dtype = 'int')

final_floor = floor.copy()
cv2.drawContours(final_floor, [new_screenCnt], -1, (255, 0, 0), 2)

plt.subplot(), plt.imshow(final_floor, cmap = 'gray')
plt.title('Final Contour'), plt.xticks([]), plt.yticks([]), plt.show()

#Crop and warp image into a rectangle
warped_cropped, tfm = four_point_transform(final_floor, new_screenCnt.reshape(4, 2)) # HOW IS GORUND CROPPED AND EXTRACT TFM FROM HERE










#just make into func to make src points so can extract tfm

plt.subplot(), plt.imshow(warped_cropped, cmap = 'gray')
plt.title('Final'), plt.xticks([]), plt.yticks([]), plt.show()

#Open and sort jsons into L/R foot position per frame
big_array = []

for keypoint_file in sorted(keypoint_files):
	data = read_keypoints(keypoint_file)
	points = find_pose_keypoints(data)
	
	if (len(points) >= 66): #If a person is detected in this frame
		x = points[19 * 3] #Left big toe
		y = points[19 * 3 + 1]
		if x == 0: #If the foot is not detected in this frame label positions as none
			L_foot = [None, None]
		else:  
			L_foot = [x, y]

		x = points[22 * 3] #Right Big toe
		y = points[22 * 3 + 1]
		if x == 0: 
			R_foot = [None, None]
		else:  
			R_foot = [x, y]

	else: #If there is no person detected label positions as none
		L_foot = [None, None]
		R_foot = [None, None]

	feet = [L_foot, R_foot]
	big_array.append(feet)
big_array = np.array(big_array)
print(big_array.shape) #Shape should be ([no. of frames, usually around 250], 2, 2)

left_array = big_array[:,0] #Take left foot position per frame and seperate into x and y
xl = left_array[:,0]
yl = left_array[:,1]
right_array = big_array[:,1] #Take right foot position per frame and seperate into x and y
xr = right_array[:,0]
yr = right_array[:,1]

fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
ax.imshow(img)#, extent=[0, 1920, 0, 1080])
ax.plot(xl, yl, 'b')
ax.plot(xr, yr, 'r')
plt.show()

'''
rectangle = (a,b,c,d)
a, b are the coordinates of the top left corner in x, y
c, d are the width and height of the rectangle respectively
'''

width = calculateDistance(top_left, top_right)
height = calculateDistance(top_left, bottom_left)

rect = (top_left[0], 
		top_left[1], 
		width, 
		height)

def rectContains(rect,pt):
    logic = rect[0] < pt[0] < rect[0] + rect[2] and rect[1] < pt[1] < rect[1]+rect[3]
    return logic


#CROP POINTS
tf_left_array = []
tf_right_array = []
for i in range(len(xl)):
	x = xl[i]
	y = yl[i]
	if x != None and y != None:
		x = x - top_left[0] - floor_top_left[0]
		y = y - top_left[1] - floor_top_left[1]
	if (x != None) and (y != None) and (x > 0) and (y > 0) and (x < (bottom_right[0] + floor_bottom_right[0])) and (y < bottom_right[1] + floor_bottom_right[1]): #remove empty points and points outside of triangle
		point = (x, y)
		tf_left_array.append(point)
tf_left_array = np.array([tf_left_array], dtype = ('float32'))

for i in range(len(xr)):
	x = xr[i]
	y = yr[i]
	if x != None and y != None:
		x = x - top_left[0] - floor_top_left[0]
		y = y - top_left[1] - floor_top_left[1]
	if (x != None) and (y != None) and (x > 0) and (y > 0) and (x < (bottom_right[0] + floor_bottom_right[0])) and (y < bottom_right[1] + floor_bottom_right[1]): #remove empty points and points outside of triangle
		point = (x, y)
		tf_right_array.append(point)
tf_right_array = np.array([tf_right_array], dtype = ('float32'))

#Apply tfm to points

tf_left_array = cv2.perspectiveTransform(tf_left_array, tfm)
tf_right_array = cv2.perspectiveTransform(tf_right_array, tfm)

xl = tf_left_array[0][:,0]
yl = tf_left_array[0][:,1]
xr = tf_right_array[0][:,0]
yr = tf_right_array[0][:,1]

fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
ax.imshow(warped_cropped)#, extent=[0, 1920, 0, 1080])
ax.plot(xl, yl, 'b')
ax.plot(xr, yr, 'r')
fig2, ax2 = plt.subplots() #Plot left and right foot trajectory in blue and red
ax2.imshow(warped_cropped)#, extent=[0, 1920, 0, 1080])
ax2.plot(xl, yl, 'b')
ax2.plot(xr, yr, 'r')
plt.show()

#create json/dictionary that includes the tfm and foot positions per frame
#big_array  [Frame, Right foot[x,y], 	Left foot[x,y]]
#			[250, 	[261, 512], 		[83, 416]]
#How many fps is videos?

#save picture in data directory of trajectories on floor to eye check
