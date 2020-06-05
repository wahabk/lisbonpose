from lisbonpose.lisbonpose import Lisbon
import cv2

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
            frame = lisbon.getFrame(vid)

            corners, labelled_corners_img = corner_labeller(frame)

            tfm = lisbon.get_tfm_2(corners)



