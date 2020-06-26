import lisbonpose
import cv2
from pathlib2 import Path
import os

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
            video = lisbon.getVideo(vidpath)
            framenum = lisbonpose.video_viewer(video)
            framenum = 0
            frame = video[framenum]

            # Label corners until success
            success = False
            while success == False:
                success, corners, labelled_image = lisbonpose.corner_labeller(frame)

            tfm = lisbon.get_tfm_2(corners)
            tfmpath = w / 'tfm.json'
            lisbon.saveJSON(tfm, tfmpath)
            tfm = lisbon.readJSON(tfmpath)
            warped = cv2.warpPerspective(frame, tfm, (500,150)) #This bit crops around rectangle

            # cv2.imshow('transformed cropped corner', warped)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            trajectories = lisbon.readJSON(trajectorypath)
            transformed_points = lisbon.transform_points(trajectories, tfm)

            # lisbon.draw_points(frame, trajectories)
            lisbon.draw_points(warped, transformed_points)


