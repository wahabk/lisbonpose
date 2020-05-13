from lisbonpose.lisbonpose import Lisbon
import cv2
import numpy as np
from pathlib2 import Path

lisbon = Lisbon()

vidspath = Path('Data/Videos/')
vidnames = [e for e in vidspath.iterdir()]

for i in vidnames:
    print(i)
    #print(i.suffix)
    #print(i.stem)
    info = i.stem.split('_')
    print(info)
    seperator = '/'
    new_path = 'Data/clean/' + seperator.join(info)
    Path(new_path).mkdir(parents=True, exist_ok=True)
    new_vidpath = Path(new_path) / i.name
    print(new_vidpath)
    i.replace(new_vidpath)


