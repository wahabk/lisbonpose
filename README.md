# lisbonpose

Lisbonpose is a project to make use of great deep learning pose prediction software like [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) and [alphapose](https://github.com/MVIG-SJTU/AlphaPose) for gait analysis research.

While pose prediction has come a long way in the past few years it is still no where near the gold standard (motion capture). So this project aims to extract foot/ankle position and transform them into 2D ground coordinates.

# Installation

## Requirements

- conda
- opencv
- PyQt5
- [Alphapose](https://github.com/MVIG-SJTU/AlphaPose)

To install please run:

```shell
git clone https://github.com/wahabk/lisbonpose
cd lisbonpose
conda env create -f environment.yml
conda activate chess
python3 -m pip install .
```

# Examples

Please look at ```examples/Lisbonpose.ipynb``` for an example on how to run lisbonpose with alphapose on Google Colab
