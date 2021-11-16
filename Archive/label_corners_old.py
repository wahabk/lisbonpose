import lisbonpose
import cv2
from pathlib2 import Path
import os
import numpy as np
import gc

def iterdir(x):
    list_ = []
    for e in x.iterdir():
        if 'DS_Store' not in str(e):
            list_.append(e)
    return list_

lisbon = lisbonpose.Lisbon()

settings = lisbon.readJSON('.settings.json').tolist()
datapath = Path(settings["dataset_path"])
peoplepaths = iterdir(datapath)
peoplepaths.sort()
conditions = ['LAC', 'LAP', 'LSC', 'LSP']

for p in peoplepaths:
    for c in conditions:
        walkpaths = p / c
        walks = iterdir(walkpaths)
        walks.sort()
        for w in walks:
            #load everything
            files = iterdir(w)
            vidpath = [f for f in files if f.suffix == '.mp4'][0]
            print('Video name: ', os.path.splitext(vidpath.stem)[0])
            trajectorypath = w / 'foot_trajectories.json'
            vidpath = str(vidpath)
            
            # skip is number of frames skipped to save on RAM
            skip = 10
            video = lisbon.getVideo(vidpath, skip = skip)
            low_res_video = np.array([cv2.resize(frame, (960, 540)) for frame in video])

            framenum = lisbonpose.video_viewer(low_res_video)
            frame = video[framenum]
            video, low_res_video = None, None
            gc.collect()

            # Label corners until success
            success = False
            while success == False:
                success, corners, labelled_image = lisbonpose.corner_labeller(frame)

            tfm = lisbon.get_tfm_2(corners)
            tfmpath = w / 'tfm.json'
            lisbon.saveJSON(tfm, tfmpath)
            warped = cv2.warpPerspective(frame, tfm, (500,150)) #This bit crops around rectangle

            trajectories = lisbon.readJSON(trajectorypath)
            transformed_points = lisbon.transform_points(trajectories, tfm)

            # lisbon.draw_points(frame, trajectories)
            lisbon.draw_points(warped, transformed_points)
            gc.collect()


