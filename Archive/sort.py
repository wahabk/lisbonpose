from lisbonpose.transform import four_point_transform
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from cropFloor import cropFloor
from pathlib import Path
import numpy as np
import argparse
import imutils
import cv2
import json

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

pointpath = Path("/home/wahab/deep_learning/op_json_output/")
keypoint_files = 	pointpath.iterdir()

big_array = []

for keypoint_file in sorted(keypoint_files):
	data = read_keypoints(keypoint_file)
	points = find_pose_keypoints(data)
	
	if (len(points) >= 66):
		x = points[19 * 3]
		y = points[19 * 3 + 1]
		if x == 0: 
			L_foot = [None, None]
		else:  
			L_foot = [x, y]

		x = points[22 * 3]
		y = points[22 * 3 + 1]
		if x == 0: 
			R_foot = [None, None]
		else:  
			R_foot = [x, y]

	else:
		L_foot = [None, None]
		R_foot = [None, None]

	feet = [L_foot, R_foot]
	big_array.append(feet)

big_array = np.array(big_array)

print(big_array.shape)

left_array = big_array[:,0]
xl = left_array[:,0]
yl = left_array[:,1]

right_array = big_array[:,1]
xr = right_array[:,0]
yr = right_array[:,1]

img = plt.imread("/home/wahab/Data/points_on_floor.png")

fig, ax = plt.subplots()

ax.imshow(img, extent=[0, 1920, 0, 1080])

ax.plot(xl, yl, 'b')
ax.plot(xr, yr, 'r')


plt.show()
