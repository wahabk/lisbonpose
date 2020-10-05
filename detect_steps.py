from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

lisbon = Lisbon()

def masks(vec):
	# From https://stackoverflow.com/questions/47342447/find-locations-on-a-curve-where-the-slope-changes?rq=1
	d = np.diff(vec)
	dd = np.diff(d)

	# Mask of locations where graph goes to vertical or horizontal, depending on vec
	to_mask = ((d[:-1] != 0) & (d[:-1] == -dd))
	# Mask of locations where graph comes from vertical or horizontal, depending on vec
	from_mask = ((d[1:] != 0) & (d[1:] == dd))
	return to_mask, from_mask

def slope(p1, p2):
	print(p1[1] ,p2)
	[x1, y1] = p1
	[x2, y2] = p2
	m = (y2-y1)/(x2-x1)
	return m

for i in range(1,2):
	person = lisbon.read(i)
	for condition, condition_data in person.items():
		for run in condition_data:
			run['name']
			tfm = run['tfm']
			traj = run['trajectories']
			frame = run['frame']

			if tfm is not None:
				transf_traj = run['transf_traj']
				warped = run['transf_img']
				lisbon.draw_points(warped, transf_traj)

				

				new_transf_traj = []
				for foot in transf_traj:
					x = savgol_filter(foot[:, 0], 17, 3)
					y = savgol_filter(foot[:, 1], 17, 3)
					foot = np.column_stack((x, y))
					new_transf_traj.append(foot)

				left = new_transf_traj[0]
				right = new_transf_traj[1]

				x_distance, y_distance = [], []
				zipped = zip(left, right)
				for (xl, yl), (xr, yr) in zipped:
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
				
				left_steps = find_peaks(x_distance, distance = 10)[0]
				no_left_steps = len(left_steps)
				print(left_steps)

				x_axis = np.zeros(250)
				steplist = [(0,x) for x in step_frame]
				plt.plot(x_distance, 'r')
				plt.plot(x_axis)
				plt.plot(left_steps, np.zeros(no_left_steps), 'go')
				#plt.axis([0, 250, -100, 100])
				plt.xlabel('frame')
				plt.ylabel('distance (pixels)')
				plt.title(f'Person: {i} Condition: {condition} X Distance between left and right foot')
				plt.show()

				

