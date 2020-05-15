from lisbonpose.lisbonpose import Lisbon
import cv2
from pathlib2 import Path

datapath = Path('Data/clean/Y/')

peoplepaths = [(e) for e in datapath.iterdir()]
print(peoplepaths)

conditions = ['LAC', 'LAP', 'LSC', 'LSP']

for p in peoplepaths:
    for c in conditions:
        walkpaths = p / c
        walks = [e for e  in walkpaths.iterdir()]
        for w in walks:
            vids = [e for e  in w.iterdir()]
            print('walk: '+str(w)+' has vids '+str(vids)+'')




'''
if not os.path.exists(directory): # Create target Directory if it doesn't already exist
    os.mkdir(directory)
    if not os.path.exists(directory_json):
        os.mkdir(directory_json)
        #print("Directory " , directory_json ,  " Created ")
        exists = False
else:
    #print("Directory " , directory_json ,  " already exists.\n")
    exists = True

#Run openpose and save jsons if they don't already exist
if not exists:
    model_folder = '--model_folder ~/deep_learning/openpose/models/'
    p = Popen('~/deep_learning/openpose/build/examples/openpose/openpose.bin '+model_folder+' --video '+vidpath+' --write_json '+directory_json+' --number_people_max 1', 
            shell=True)
    p.wait()
    p.communicate()
'''