from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

lisbon = Lisbon()

def combine(list1, list2):
	# if list1[0,0] < list2[0,0]: index1 = True
	# else: left_first = False
	first = list1
	second = list2
	result = [None]*(len(list1)+len(list2))
	result[::2] = first
	result[1::2] = second
	return result

def detect_steps(traj):
	'''
	Takes transformed (flat) foot trajectories and finds steps using peaks and troughs 
	of distance between feet in x axis (because foot x distance is largest when a step is taken)
	'''
	new_transf_traj = []
	# make a smoothed transformed_trahectory
	for foot in traj:
		# Use savgol filter to smooth foot trajectory for step detection
		x = savgol_filter(foot[:, 0], 17, 3)
		y = savgol_filter(foot[:, 1], 17, 3)
		# reformat to fit previous format
		foot = np.column_stack((x, y))
		new_transf_traj.append(foot)

	# reformat trajectory for finding x
	left = new_transf_traj[0]
	right = new_transf_traj[1]
	zipped_traj = zip(left, right)
	x_distance, y_distance = [], []
	
	for (xl, yl), (xr, yr) in zipped_traj:
		x_distance.append(xl - xr)
		y_distance.append(yl - yr)
	x_distance = np.array(x_distance)

	'''
	This section constructs a list of two lists 'steps = [left, right]' 
	each is a list of frames where the foot steps

	TODO remove nans from xdistance
	'''

	left, left_dict = find_peaks(x_distance, height=10, distance=25)
	right, right_dict = find_peaks(-x_distance, height=10, distance=25)
	no_steps = len(left) + len(right)
	steps = [left, right]

	# constuct list of xy positions for steps of each foot
	stepsXY = []
	for i, foot in enumerate(steps):
		footXY = []
		for j, frame in enumerate(foot):
			stepXY = transf_traj[i,frame]
			footXY.append(stepXY)
		footXY = np.array(footXY)
		stepsXY.append(footXY)
	stepsXY=np.array(stepsXY)

	return steps, stepsXY, x_distance

def find_step_LW(stepsXY):
	stepXY_dist = []
	left = stepsXY[0]
	right = stepsXY[1]





	for foot in stepsXY:
		footXY_dist = []
		for i, step in enumerate(foot[:-1]):
			# if i == len(foot): continue
			x1, y1 = foot[i]
			x2, y2 = foot[i+1]

			footXY_dist.append((x1 - x2, y1 - y2))
		stepXY_dist.append(footXY_dist)
	return np.array(stepXY_dist)







for i in range(1,2): # for each person on local data
	person = lisbon.read(i)
	for condition, condition_data in person.items():
		for run in condition_data:
			run['name']
			tfm = run['tfm']
			frame = run['frame']

			if tfm is not None:
				print(run.keys())
				transf_traj = run['transf_traj']
				warped = run['transf_img']
				
				steps, stepsXY, x_distance = detect_steps(transf_traj)
				stepXY_dist = find_step_LW(stepsXY)

				left = steps[0]
				right = steps[1]
				x_axis = np.zeros(250)
				plt.plot(x_distance, 'g')
				plt.plot(x_axis)
				plt.plot(left, np.zeros(len(left)), 'bo')
				plt.plot(right, np.zeros(len(right)), 'ro')
				#plt.axis([0, 250, -100, 100])
				plt.xlabel('frame')
				plt.ylabel('distance (pixels)')
				plt.title(f'Person: {i} Condition: {condition} X Distance between left and right foot')
				plt.show()

				print(f'\n {stepXY_dist}')

				image = lisbon.draw_points(warped, transf_traj, steps = stepsXY)

				list1 = ['f', 'o', 'o']
				list2 = ['hello', 'world']
				print(combine(list1, list2))

				# extract functions from this
				# Find number of steps, step length, and step width

