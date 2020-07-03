from lisbonpose.lisbonpose import Lisbon
import numpy as np
import matplotlib.pyplot as plt

lisbon = Lisbon()

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

				#lisbon.draw_points(warped, transf_traj)
				
				left = transf_traj[0]
				right = transf_traj[1]
				zipped = zip(left, right)

				x_distance, y_distance = [], []
				for (xl, yl), (xr, yr) in zipped:
					x_distance.append(xl - xr)
					y_distance.append(yl - yr)
				
				x_distance = np.array(x_distance)
				y_distance = np.array(y_distance)




				step_frame = [] # list of frames where a step is detected

				for i in range(0, x_distance.shape[0]-1):
					step = False
					x1 = x_distance[i]
					x2 = x_distance[i+1]
					if (x1 < 0 and x2 > 0) or (x1 > 0 and x2 < 0):
						step_frame.append(i)
						step = True

				x_axis = np.zeros(250)
				steplist = [(0,x) for x in step_frame]
				print(x_distance)
				plt.plot(x_distance, 'r')
				plt.plot(y_distance, 'b')
				plt.plot(x_axis)
				plt.plot(step_frame, np.zeros(len(step_frame)), 'go')

				#plt.axis([0, 250, -100, 100])
				plt.xlabel('frame')
				plt.ylabel('distance (pixels)')
				plt.title('Histogram of IQ')
				plt.show()

				






