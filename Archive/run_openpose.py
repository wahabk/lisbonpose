import sys
import os
import subprocess
from subprocess import Popen
from sys import platform
import cv2
from os import listdir
from os.path import isfile, join
import sched, time

def go(str):
	print(str)
'''
scheduler = sched.scheduler(time.time, time.sleep)
print('Set to run at 21:15, please dont turn off :)')
scheduler.enter(18000, 1, go, ('go!!!',))
scheduler.run()
'''

experiment = ['Control', 'Lisbon']
for e in experiment:
	path = '/home/wahab/Desktop/Wahab/Data/greig_corridor_data/'+e+''
	filenames = [f for f in listdir(path) if isfile(join(path, f))]
	
	for video in filenames:
		vid = video[:-4] #remove .mp4
		vidpath = 			"./Data/greig_corridor_data/"+e+"/"+vid+".mp4"
		directory = 		"./Data/"+e+"/"+vid+""
		directory_json = 	""+directory+"/json/"

		#Make folders
		if not os.path.exists(directory): # Create target Directory if it doesn't already exist
			os.mkdir(directory)
			if not os.path.exists(directory_json):
				os.mkdir(directory_json)
				#print("Directory " , directory_json ,  " Created ")
				exists = False
		else:
			#print("Directory " , directory_json ,  " already exists")
			exists = True

		#Run openpose and save jsons
		model_folder = '--model_folder ~/deep_learning/openpose/models/'
		p = Popen('~/deep_learning/openpose/build/examples/openpose/openpose.bin '+model_folder+' --video '+vidpath+' --write_json '+directory_json+' --number_people_max 1 --display -1', 
				shell=True)
		p.wait()
		p.communicate()

#subprocess.call(['shutdown', '-h'])