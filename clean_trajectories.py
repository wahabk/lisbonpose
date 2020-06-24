from lisbonpose.lisbonpose import Lisbon
import cv2
import numpy as np
from pathlib2 import Path
import json

iterdir = lambda x : [e for e  in x.iterdir()]

lisbon = Lisbon()

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
            vid = [str(f) for f in files if f.suffix == '.mp4']
            print(vid[0])
            image = lisbon.getFrame(vid[0])
            pointpath = w / 'Points/'
            jsons = [e for e in pointpath.iterdir()]
            trajectories = lisbon.read_sort_keypoints(jsons)

            
            # lisbon.draw_points(image, trajectories)

            # image = cv2.resize(image, (0,0), fx=0.8, fy=0.8) 

            # corners = lisbon.detect_chess(image)

            # # square = lisbon.draw_chess(image, corners)
            # # # cv2.imshow('drawn chess', square)
            # # # cv2.waitKey()

            # # tfm = lisbon.get_tfm(image, corners)

            # # warped = cv2.warpPerspective(image, tfm, (1920, 1080)) #This bit crops around rectangle
            # # warped = cv2.resize(warped, (0,0), fx=0.5, fy=0.5) 

            # # transformed_points = lisbon.transform_points(trajectories, tfm)

            # # lisbon.draw_points(warped, transformed_points)

            jsonpath = w / 'foot_trajectories.json'
            with open(str(jsonpath), 'w') as json_file:
                json.dump(trajectories.tolist(), json_file)




