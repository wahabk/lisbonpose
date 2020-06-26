from lisbonpose.lisbonpose import Lisbon
import numpy as np
from pathlib2 import Path

lisbon = Lisbon()

for i in range(1,2):
	person = lisbon.read(i)
	for condition, condition_data in person.items():
		for run in condition_data:
			print(run['name'])
			print(run['tfm'])
			print(run['trajectories'])
			lisbon.imshow(run['frame'])



