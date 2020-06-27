import lisbonpose
import cv2
from pathlib2 import Path
import os
import numpy as np
import gc

lisbon = lisbonpose.Lisbon()

for i in range(1,3):
	person = lisbon.read(i)
	for condition, condition_data in person.items():
		for run in condition_data:
			print(run['name'])
			tfm = run["tfm"]
			trajectories = run['trajectories']
			frame = run['frame']
			vidpath = run['vidpath']
			tfmpath = run['tfmpath']

			# skip is number of frames skipped to save on RAM
			skip = 10
			video = lisbon.getVideo(vidpath, skip = skip)
			low_res_video = np.array([cv2.resize(frame, (960, 540)) for frame in video])

			print('\nviewing')
			framenum = lisbonpose.video_viewer(low_res_video)
			# import pdb
			# pdb.set_trace()
			frame = video[framenum]
			video, low_res_video = None, None
			gc.collect()

			# Label corners until success
			success = False
			while success == False:
				success, corners = lisbonpose.corner_labeller(frame)

			tfm = lisbon.get_tfm_2(corners)
			lisbon.saveJSON(tfm, tfmpath)
			warped = cv2.warpPerspective(frame, tfm, (500,150)) #This bit crops around rectangle

			transformed_points = lisbon.transform_points(trajectories, tfm)

			# lisbon.draw_points(frame, trajectories)
			lisbon.draw_points(warped, transformed_points)

			success, corners, labelled_image = None, None, None
			gc.collect()


