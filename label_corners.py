import lisbonpose
import cv2
from pathlib2 import Path
import os

iterdir = lambda x : [e for e  in x.iterdir()]

lisbon = lisbonpose.Lisbon()

datapath = Path('Data/clean/')
peoplepaths = [e for e in datapath.iterdir()]
peoplepaths.sort()
conditions = ['LAC', 'LAP', 'LSC', 'LSP']

for p in peoplepaths:
    for c in conditions:
        walkpaths = p / c
        walks = iterdir(walkpaths)
        walks.sort()
        for w in walks:
            files = iterdir(w)
            vidpath = [f for f in files if f.suffix == '.mp4'][0]
            print('Video name: ', os.path.splitext(vidpath.stem)[0])
            vidpath = str(vidpath)
            framenum = lisbonpose.video_viewer(vidpath)
            frame = lisbon.getFrame(vidpath, framenum)

            success = False
            while success == False:
                success, corners, labelled_image = lisbonpose.corner_labeller(frame)

            tfm = lisbon.get_tfm_2(corners)
            warped = cv2.warpPerspective(labelled_image, tfm, (500,150)) #This bit crops around rectangle
            
            cv2.imshow('transformed cropped corner, if unhappy write down name', warped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            jsonpath = w / 'tfm.json'
            lisbon.saveJSON(tfm, jsonpath)




