from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from math import sqrt
import csv

lisbon = Lisbon()

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
	footless = []
	for i, foot in enumerate(steps):
		footXY = []
		for frame in foot:
			stepXY = transf_traj[i,frame]
			footXY.append(stepXY)
			footless.append(stepXY)
		footXY = np.array(footXY)
		stepsXY.append(footXY)
	stepsXY=np.array(stepsXY)
	footless=np.array(footless)

	return no_steps, steps, stepsXY, x_distance, footless

def find_step_LW(stepsXY):
	
	stepXY_dist = []
	for i, step in enumerate(stepsXY[:-1]):
		# if i == len(step): continue
		x1, y1 = stepsXY[i]
		x2, y2 = stepsXY[i+1]

		stepXY_dist.append((float(sqrt((x2 - x1)**2)), float(sqrt((y2 - y1)**2))))
	return np.array(stepXY_dist, dtype='float32')

for i in range(1,26): # for each person on local data
	person = lisbon.read(i)
	data = []
	heading = ['Participant', 'condition', 'Walk', '# Steps', 'Step Length MEAN', 'Step Length STD', 'Step Width MEAN', 'Step Width STD']
	data.append(heading)
	for condition, condition_data in person.items():
		for run in condition_data:
			run_names = run['name'].split('/')
			print(run_names)
			tfm = run['tfm']
			frame = run['frame']

			if tfm is not None:
				transf_traj = run['transf_traj']
				warped = run['transf_img']
				
				no_steps, steps, stepsXY, x_distance, footless = detect_steps(transf_traj)
				stepXY_dist = find_step_LW(footless)

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
				# plt.show()

				# image = lisbon.draw_points(warped, transf_traj, steps = stepsXY)
				print('stepXY ', stepXY_dist)

				# extract functions from this
				# Find number of steps, step length, and step width
				step_lengths = [x for x, y in stepXY_dist]
				step_widths = [y for x, y in stepXY_dist]
				d = run_names[2:] + [no_steps, np.mean(step_lengths), np.std(step_lengths), np.mean(step_widths), np.std(step_widths)]
				data.append(d)
	
	with open('final_data.csv', mode='w') as f:
		employee_writer = csv.writer(f, delimiter=',')
		for row in data:
			employee_writer.writerow(row)

