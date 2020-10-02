import lisbonpose
import cv2
from pathlib2 import Path
import numpy as np

lisbon = lisbonpose.Lisbon()

while True:
	i = input('Which person to analyse?')
	person = lisbon.read(int(i))
	for condition, condition_data in person.items():
		for run in condition_data:
			print(run['name'])
			trajectories = run['trajectories']
			vidpath = run['vidpath']
			tfmpath = run['tfmpath']
			# skip is number of frames skipped to save on RAM
			skip = 60
			video = lisbon.getVideo(vidpath, skip = skip)
			low_res_video = np.array([cv2.resize(frame, (960, 540)) for frame in video])

			framenum = lisbonpose.video_viewer(low_res_video)
			frame = video[framenum]

			# Label corners until success
			success = False
			while success == False:
				success, corners = lisbonpose.corner_labeller(frame)

			tfm = lisbon.get_tfm_2(corners)
			lisbon.saveJSON(tfm, tfmpath)

			# warped = cv2.warpPerspective(frame, tfm, (500,150)) #This bit crops around rectangle
			# transformed_points = lisbon.transform_points(trajectories, tfm)
			# lisbon.draw_points(warped, transformed_points)
				



