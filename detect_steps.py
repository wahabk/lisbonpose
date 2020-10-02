from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt

lisbon = Lisbon()

def zero_not_hero(yolo):
	yolo2 = []
	for x in yolo:
		if x == 0: x = None
		yolo2.append(x)
	return yolo2

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

				left = transf_traj[0]
				right = transf_traj[1]
				print(left.shape)
				
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
				
				total_step_n = len(step_frame)

				x_axis = np.zeros(250)
				steplist = [(0,x) for x in step_frame]
				plt.plot(x_distance, 'r')
				plt.plot(x_axis)
				plt.plot(step_frame, np.zeros(total_step_n), 'go')
				#plt.axis([0, 250, -100, 100])
				plt.xlabel('frame')
				plt.ylabel('distance (pixels)')
				plt.title(f'Person: {i} Condition: {condition} X Distance between left and right foot')
				plt.show()

				

