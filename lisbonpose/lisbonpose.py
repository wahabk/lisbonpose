from pathlib2 import Path
import numpy as np
import json
import cv2
import os

class Lisbon():
	def __init__(self):
		pass

	def read_sort_keypoints(self, keypoint_file):
		# Open and sort jsons into L/R foot position per frame
		feet_array = []

		for keypoint_file in sorted(keypoint_files):
			points = read_pose_points(keypoint_file)
			
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
			feet_array.append(feet)
		feet_array = np.array(feet_array)

		left_array = feet_array[:,0] #Take left foot position per frame and seperate into x and y
		right_array = feet_array[:,1] #Take right foot position per frame and seperate into x and y
		xl = left_array[:,0]
		yl = left_array[:,1]
		xr = right_array[:,0]
		yr = right_array[:,1]

		return [left_array, right_array]

	def read_pose_points(self, keypoint_filename):
		keypoint_file = keypoint_filename.open()
		keypoint_data = json.load(keypoint_file)
		keypoint_file.close()

		keypoints = keypoint_data['people']
		if (len(keypoints) >= 1):
			keypoints = keypoints[0] # first person
			keypoints = keypoints['pose_keypoints_2d'] # body points in body25 model
			return keypoints
		else:
			return []

	def getFrame(self, videofile, frame=1):
		vidcap = cv2.VideoCapture(videofile)
		vidcap.set(1, frame-1)
		success, img = vidcap.read()
		if not success: 
			raise Exception("Could not load image! :(")
		return img

	def detect_chess(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		ret, thresh = cv2.threshold(gray, 100, 150, cv2.THRESH_BINARY)
		ret, corners = cv2.findChessboardCorners(thresh, (9,6), None)

		top_left 	 = corners[ 0][0]
		top_right 	 = corners[ 8][0]
		bottom_left  = corners[45][0]
		bottom_right = corners[53][0]

		corners = np.array([
			top_left,
			bottom_left,
			bottom_right,
			top_right
			], dtype = 'int32')

		return corners.reshape(4, 2)

	def draw_chess(self, image, corners):
		return cv2.polylines(image, np.int32([corners]), 1, (0,0,255), 4)

	def get_tfm(self, image, corners):
		src, dst = self.get_src_dst(image, corners)
		dst = dst + 5000
		tfm = cv2.getPerspectiveTransform(src, dst)
		return tfm

	def get_src_dst(self, image, pts):
		# obtain a consistent order of the points and unpack them
		# individually

		rect = np.zeros((4, 2), dtype = "float32")
		s = pts.sum(axis = 1)
		rect[0] = pts[np.argmin(s)]
		rect[2] = pts[np.argmax(s)]
		diff = np.diff(pts, axis = 1)
		rect[1] = pts[np.argmin(diff)]
		rect[3] = pts[np.argmax(diff)]

		(tl, tr, br, bl) = rect

		# compute the width of the new image, which will be the
		# maximum distance between bottom-right and bottom-left
		# x-coordiates or the top-right and top-left x-coordinates
		widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
		widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
		maxWidth = max(int(widthA), int(widthB))

		# compute the height of the new image, which will be the
		# maximum distance between the top-right and bottom-right
		# y-coordinates or the top-left and bottom-left y-coordinates
		heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
		heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
		maxHeight = max(int(heightA), int(heightB))

		# now that we have the dimensions of the new image, construct
		# the set of destination points to obtain a "birds eye view",
		# (i.e. top-down view) of the image, again specifying points
		# in the top-left, top-right, bottom-right, and bottom-left
		# order
		dst = np.array([
			[0, 0],
			[maxWidth - 1, 0],
			[maxWidth - 1, maxHeight - 1],
			[0, maxHeight - 1]], dtype = "float32")

		# return the source and destination points
		return rect, dst


	def transform_points(self, points, tfm):
		pass
		return transformed_points

	def save_points(self, points):
		pass

	def draw_points(self, image, points):
		pass