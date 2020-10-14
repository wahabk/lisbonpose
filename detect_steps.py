from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

lisbon = Lisbon()


for i in range(1,2): # for each person on local data
	person = lisbon.read(i)
	for condition, condition_data in person.items():
		for run in condition_data:
			run['name']
			tfm = run['tfm']
			frame = run['frame']

			if tfm is not None:
				transf_traj = run['transf_traj']
				warped = run['transf_img']
				

				
				# make a smoothed transformed_trahectory
				new_transf_traj = []
				for foot in transf_traj:
					x = savgol_filter(foot[:, 0], 17, 3)
					y = savgol_filter(foot[:, 1], 17, 3)
					foot = np.column_stack((x, y))
					new_transf_traj.append(foot)

				left = new_transf_traj[0]
				right = new_transf_traj[1]
				zipped_traj = zip(left, right)
				x_distance, y_distance = [], []
				
				for (xl, yl), (xr, yr) in zipped_traj:
					x_distance.append(xl - xr)
					y_distance.append(yl - yr)
				
				x_distance = np.array(x_distance)
				step_frame = [] # list of frames where a step is detected

				for j in range(0, x_distance.shape[0]-1):
					step = False
					x1 = x_distance[j]
					x2 = x_distance[j+1]
					if (x1 < 0 and x2 > 0) or (x1 > 0 and x2 < 0):
						step_frame.append(j)
						step = True


				# y = x_distance
				# x = np.arange(x_distance.shape[0])
				# curve = np.column_stack((x, y))
				
				'''
				This section constructs a list 'steps = [left, right]' which contains
				two lists of frames that each foot steps
				'''
				#TODO remove nans from xdistance
				left, left_dict = find_peaks(x_distance, height=10, distance=25)
				right, right_dict = find_peaks(-x_distance, height=10, distance=25)
				no_steps = len(left) + len(right)
				steps = [left, right]

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

				#construct a list of x-distance between each step
				image = lisbon.draw_points(warped, transf_traj, steps = stepsXY)

