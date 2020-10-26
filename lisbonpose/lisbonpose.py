from pathlib2 import Path
import numpy as np
import json, codecs
import cv2
import os
import matplotlib.pyplot as plt
import time

class Lisbon():
	'''
	Class for reader, writer, viewer etc

	encapsulates helper/utility funvtions

	'''
	def __init__(self, path = './Data/clean/'):
		self.dataset_path = path

	def read(self, n):
		'''
		Read each person dictionary, which contains list of runs for each condition
		'''
		
		print('Reading participant', n)
		datapath = Path(self.dataset_path)
		all_paths = self.iterdir(datapath)
		all_paths.sort()
		conditions = ['LAC', 'LAP', 'LSC', 'LSP']
		p = all_paths[n-1] # Path for folder in participant

		person_dict = {}
		condition_list = []


		for c in conditions:
			condition_path = p / c
			runs = self.iterdir(condition_path)
			runs.sort()
			for run in runs:
				files = self.iterdir(run)
				vid = [str(f) for f in files if f.suffix == '.mp4']
				
				vid_path = vid[0]
				points_path = run / 'Points/'
				tfm_path = run / 'tfm.json'
				trajectory_path = run / 'foot_trajectories.json'
				
				frame = self.getFrame(vid[0])
				try:
					tfm = self.readJSON(tfm_path)
				except:
					print('Not reading this TFM as its not available: ', str(run))
					tfm = None
				trajectories = self.readJSON(trajectory_path)

				run_dict = {
					'name' : str(run),
					'condition' : c,
					'frame': frame, 
					# 'trajectories': trajectories,
					'tfm': tfm,
					'vidpath' : vid_path,
					'tfmpath' : tfm_path
				}

				# Optional
				if tfm is not None:
					transformed_trajectories = self.transform_points(trajectories, tfm)
					warped = cv2.warpPerspective(frame, tfm, (500,150)) #This bit crops around rectangle
					transformed_trajectories[transformed_trajectories <= 20] = None
					run_dict['transf_traj'] = transformed_trajectories
					run_dict['transf_img'] = warped
					

				condition_list.append(run_dict)
			person_dict[c] = condition_list

		return person_dict

	def getFrame(self, videofile, frame=1):
		cap = cv2.VideoCapture(videofile)
		cap.set(1, frame-1)
		success, img = cap.read()
		if not success: 
			raise Exception("Could not load image! :(")
		cap.release()
		return img

	def getVideo(self, video_path, skip = 1):
		cap = cv2.VideoCapture(video_path)
		cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
		length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
		video_length = int(length)-12

		video = []
		
		for i in range(0, video_length-10, skip):
			print('Reading video frame ', i, end="\r")
			cap.set(1, i)
			success, frame = cap.read()
			#frame = cv2.resize(frame, (960, 540))  
			video.append(frame)
			if not success:
				raise Exception(f"Could not load video, failed on frame {i}, video length is {video_length} frames.")
		
		cap.release()
		return np.array(video)

	def read_pose_points(self, keypoint_filename):
		
		print(keypoint_filename)
		with open(keypoint_filename) as f:
			keypoint_data = json.load(f)
		
		

		keypoints = keypoint_data['people']
		if (len(keypoints) >= 1):
			keypoints = keypoints[0] # first person
			keypoints = keypoints['pose_keypoints_2d'] # body points in body25 model
			return keypoints
		else:
			return []

	def read_sort_keypoints(self, keypoint_files):
		# Open and sort jsons into L/R foot position per frame
		feet_array = []

		for keypoint_file in sorted(keypoint_files):
			points = self.read_pose_points(keypoint_file)
			
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
		
		# xl = left_array[:,0]
		# yl = left_array[:,1]
		# xr = right_array[:,0]
		# yr = right_array[:,1]

		return np.array([left_array, right_array])

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
		dst = dst + 6000
		tfm = cv2.getPerspectiveTransform(src, dst)
		return tfm

	def get_tfm_2(self, corners):
		'''
			Get homography transformation from corners of mat
			Corners are considered as source points and destination 
			points are the dimensions of the mat

			corners is in order TL, TR, BR, BL 
		'''
		src = np.array([
			corners[1],
			corners[2],
			corners[3],
			corners[0]], dtype = "float32")

		w = 500
		h = 150

		dst = np.array([
			[0, 0],
			[w, 0],
			[w, h],
			[0, h]], dtype = "float32")

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
		points = points #+6000
		tfm = np.array(tfm, dtype = "float32")
		
		# format points for cv2
		right_array 	= np.array([points[0]], dtype = ('float32'))
		left_array 		= np.array([points[1]], dtype = ('float32'))
		#Apply tfm to points
		tf_left_array 	= cv2.perspectiveTransform(left_array, tfm)
		tf_right_array 	= cv2.perspectiveTransform(right_array, tfm)
		transformed_points = np.array([tf_left_array[0], tf_right_array[0]])

		return transformed_points

	def draw_points(self, image, points, steps=None):
		left_array = points[0]
		xl = left_array[:,0]
		yl = left_array[:,1]

		right_array = points[1]
		xr = right_array[:,0]
		yr = right_array[:,1]

		fig, ax = plt.subplots()
		ax.imshow(image )#, extent=[0, 1920, 0, 1080])
		ax.plot(xl, yl, '-b.')
		ax.plot(xr, yr, '-r.')
		if steps is not None:
			left_array = steps[0]
			xl = left_array[:,0]
			yl = left_array[:,1]

			right_array = steps[1]
			xr = right_array[:,0]
			yr = right_array[:,1]
			ax.scatter(xl, yl, s=500, c='c', marker='X')
			ax.scatter(xr, yr, s=500, c='m', marker='X')
		plt.show()
		plt.close(fig)

	def saveJSON(self, nparray, jsonpath):
		json.dump(nparray.tolist(), codecs.open(jsonpath, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

	def readJSON(self, jsonpath):
		obj_text = codecs.open(jsonpath, 'r', encoding='utf-8').read()
		obj = json.loads(obj_text)
		return np.array(obj)

	def imshow(self, img):
		timestr = time.strftime("%Y%m%d-%H%M%S")
		cv2.imshow('Press <S> to save, or any other key to quit.', img)
		c = cv2.waitKey(0)
		if 's' == chr(c & 255):
			cv2.imwrite('.output/'+timestr+'.png', img)
			print(save_name, 'successfuly saved.')
		

	def iterdir(self, x):
		# This is a custom of iterdir that gets rid of weird mac ds_store files
		return [e for e in x.iterdir() if 'DS_Store' not in str(e)]

