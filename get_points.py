from lisbonpose.lisbonpose import Lisbon
import cv2
from pathlib2 import Path
from subprocess import Popen

def run_OP(vidpath, pointspath):
    if pointspath.exists():
        print(pointspath, '--- ALREADY EXISTS\n\n')
    pointspath.mkdir(exist_ok=True)
    model_folder = '--model_folder ~/code/openpose/models/'
    print('\nrunning:', '~/code/openpose/build/examples/openpose/openpose.bin '+model_folder+' --video '+str(vidpath)+' --write_json '+str(pointspath)+' --number_people_max 1\n')
    p = Popen('~/code/openpose/build/examples/openpose/openpose.bin '+model_folder+' --video '+str(vidpath)+' --write_json '+str(pointspath)+' --number_people_max 1 --display 0 --render_pose 0', 
            shell=True)
    p.wait()
    p.communicate()

datapath = Path('Data/clean/')
peoplepaths = [e for e in datapath.iterdir()]
peoplepaths.sort()
conditions = ['LAC', 'LAP', 'LSC', 'LSP']

for p in peoplepaths:
    for c in conditions:
        walkpaths = p / c
        walks = [e for e  in walkpaths.iterdir()]
        walks.sort()
        for w in walks:
            vids = [e for e  in w.iterdir()]
            for v in vids: 
                if v.suffix == '.mp4':
                    vidpath = v
                    vidname = v.stem
                    pointspath = v.parent / 'Points'
                    run_OP(vidpath, pointspath)


