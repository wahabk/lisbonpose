from lisbonpose.lisbonpose import Lisbon
import cv2
import numpy as np
from pathlib2 import Path
import json
import matplotlib.pyplot as plt

iterdir = lambda x : [e for e  in x.iterdir()]

lisbon = Lisbon()

datapath = Path('Data/clean/Y/')
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
            vid = [str(f) for f in files if f.suffix == '.mp4'][0]
            image = lisbon.getFrame(vid)

            jsonpath = w / 'foot_trajectories.json'
            with open(jsonpath) as json_file:
                trajectories = json.load(json_file)
            trajectories = np.array(trajectories)

            corners = lisbon.detect_chess(image)
            square = lisbon.draw_chess(image, corners)
            tfm = lisbon.get_tfm(image, corners)
            transformed_points = lisbon.transform_points(trajectories, tfm)
            warped = cv2.warpPerspective(image, tfm, (8000, 7000)) #This bit crops around rectangle
            #warped = cv2.resize(warped, (0,0), fx=0.5, fy=0.5) 

            lisbon.draw_points(image, trajectories)
            lisbon.draw_points(warped, transformed_points)

            # left_array = trajectories[0]
            # xl = left_array[:,0]
            # yl = left_array[:,1]

            # right_array = trajectories[1]
            # xr = right_array[:,0]
            # yr = right_array[:,1]

            # #Show and save trajectory over image
            # fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
            # ax.plot(xl, yl, '-b.')
            # ax.plot(xr, yr, '-r.')
            # plt.xlim(right=1920) #xmax is your value
            # plt.xlim(left=0) #xmin is your value
            # plt.ylim(top=0) #ymax is your value
            # plt.ylim(bottom=1080) #ymin is your value
            # plt.show()

            # print(trajectories, '\n\n\n', transformed_points)
            # left_array = transformed_points[0]
            # xl = left_array[:,0]
            # yl = left_array[:,1]

            # right_array = transformed_points[1]
            # xr = right_array[:,0]
            # yr = right_array[:,1]

            # #Show and save trajectory over image
            # fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
            # ax.plot(xl, yl, '-b.')
            # ax.plot(xr, yr, '-r.')
            # # plt.xlim(right=7000) #xmax is your value
            # # plt.xlim(left=6000) #xmin is your value
            # # plt.ylim(top=6000) #ymax is your value
            # # plt.ylim(bottom=7000) #ymin is your value
            # plt.show()