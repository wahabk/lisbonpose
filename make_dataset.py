from lisbonpose.lisbonpose import Lisbon
import cv2
from pathlib2 import Path

lisbon = Lisbon()

vidspath = Path('Data/Videos/')
vidnames = [e for e in vidspath.iterdir()]
print(vidnames)