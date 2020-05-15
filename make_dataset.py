from lisbonpose.lisbonpose import Lisbon
import cv2
import numpy as np
from pathlib2 import Path

lisbon = Lisbon()

vidspath = Path('Data/Videos/')
vidnames = [e for e in vidspath.iterdir()]

for i in vidnames:
    #print(i.suffix)
    #print(i.stem)
    info = i.stem.split('_')
    info.pop() 
    seperator = '/'
    new_path = 'Data/clean/' + seperator.join(info)
    Path(new_path).mkdir(parents=True, exist_ok=True)
    new_vidpath = Path(new_path) / i.name
    if not new_vidpath.exists():
        with new_vidpath.open(mode='xb') as fid:
            fid.write(i.read_bytes())
    #i.replace(new_vidpath)

