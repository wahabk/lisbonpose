import numpy as np
import cv2
import sys
import os

def getFrame(videofile, frame=1):
    vidcap = cv2.VideoCapture(videofile)
    vidcap.set(1, frame-1)
    success, img = vidcap.read()
    if not success: 
    	raise Exception("Could not load image! :(")
    return img

vidpath = sys.argv[1]
frame = int(sys.argv[2])
img = getFrame(vidpath, frame)
name = os.path.basename(vidpath)
save_name = '.'.join(name.split('.')[:-1]) + '_frame.png'
cv2.imshow('Press <S> to save, or any other key to quit.', img)
c = cv2.waitKey(0)
if 's' == chr(c & 255):
    cv2.imwrite('../Data/'+save_name+'', img), print(save_name, 'successfuly saved.')
else: exit()