from 	pyimagesearch.transform import four_point_transform
from 	os.path 				import isfile, join
from 	PIL 					import Image, ImageDraw
import 	matplotlib.pyplot 		as plt
from 	subprocess 				import Popen
from 	pathlib 				import Path
from 	os 						import listdir
import 	numpy 					as np
import 	argparse
import 	imutils
import 	json
import 	math
import 	cv2
import 	os

# Functions ////////////////////////////////////

def read_keypoints(keypoint_filename): #Open openpose JSON
	keypoint_file = keypoint_filename.open()
	keypoint_data = json.load(keypoint_file)
	keypoint_file.close()
	return keypoint_data

def find_pose_keypoints(keypoint_data): #Extract foot position from JSONs
	keypoints = keypoint_data['people']
	if (len(keypoints) >= 1):
		keypoints = keypoints[0] # first person
		keypoints = keypoints['pose_keypoints_2d'] # body points in body25 model
		return keypoints
	else:
		return []

def getFrame(videofile, framenum=1):
    vidcap = cv2.VideoCapture(videofile)
    vidcap.set(1, framenum-1)
    success, img = vidcap.read()
    if not success: 
    	raise Exception("Could not load image! "+videofile+"")
    return img

def cropFloor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('/home/wahab/Data/template.jpg', 0)
    template = template.astype(np.uint8)

    x, y = template.shape[::-1]

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + x, top_left[1] + y)
    
    cv2.rectangle(gray, top_left, bottom_right, 255, 2)
    cropped = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return cropped#, top_left, bottom_right

def slope(point1, point2):
	m = (point2[1] - point1[1])/(point2[0] - point1[0])
	return m

def getC(point, m):
	c =  point[1] - (m * point[0])
	return c

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('Lines do not intersect.')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

def calculateDistance(point1, point2):  
     dist = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)  
     return dist

def zero_not_hero(yolo):
	yolo2 = []
	for x in yolo:
		if x == 0: x = None
		yolo2.append(x)
	return yolo2

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print('Done :)')

# Start ///////////////////////////////////////////////////////////////////

repeat			=	['1', '2']
exp 			=	["Control", "Lisbon"]
eriment 		= 	1					# 0 for control and 1 for lisbon
length 			= 	101

printProgressBar(0, length, prefix = exp[eriment], suffix = '', length = 40)

for i in range(1, 101):
	number 			= 	str(i).zfill(3)
	#if eriment 	== 	0: if number in [] : continue #Skip these for Control
	#elif eriment 	== 	1: if number in ['039'] : continue #Skip these for Lisbon

	for r in repeat:
		
		vid 			= 	""+number+"_"+exp[eriment]+"_"+r+"" #Which video

		# DEFINE PATHS
		vidpath 		= 	"/home/wahab/Data/greig_corridor_data/"+exp[eriment]+"/"+vid+".mp4"
		directory 		= 	"Data/"+exp[eriment]+"/"+vid+""
		directory_json 	= 	""+directory+"/json/"
		pointpath 		= 	Path(directory_json)
		if eriment 	== 0: 	tfmpath = "Data/TFM/030_"+exp[eriment]+"_1.csv"
		else:				tfmpath	= "Data/TFM/001_"+exp[eriment]+"_1.csv"

		#Make folders
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

		#OPEN FILES
		keypoint_files 	= 	pointpath.iterdir()
		img 		   	= 	getFrame(vidpath, framenum = 1)
		img 		   	= 	cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		tfm 		   	=	np.loadtxt(open(tfmpath, "rb"), delimiter = ",", skiprows=0, dtype='float32')

		#Initial Analysis
		floor 			= 	cropFloor(img)
		gray 			= 	cv2.cvtColor(floor, cv2.COLOR_BGR2GRAY).astype('uint8')
		blurred 		= 	cv2.GaussianBlur(gray, (7, 7), 0) #Blur
		thresh 			= 	cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)[1] #Threshold
		edged 			= 	cv2.Canny(thresh, 2, 2) #Find edges
		img_name 		= 	'Data/'+exp[eriment]+'/'+vid+'/'+vid+'_frame.png'
		cv2.imwrite(img_name, img)

		#Open and sort jsons into L/R foot position per frame
		big_array = []

		for keypoint_file in sorted(keypoint_files):
			data = read_keypoints(keypoint_file)
			points = find_pose_keypoints(data)
			
			if (len(points) >= 66): #If a person is detected in this frame
				x = points[19 * 3] #Left big toe
				y = points[19 * 3 + 1]
				if x == 0: #If the foot is not detected in this frame label positions as none
					L_foot = [None, None]
				else:  
					L_foot = [x, y]

				x = points[22 * 3] #Right Big toe
				y = points[22 * 3 + 1]
				if x == 0: 
					R_foot = [None, None]
				else:  
					R_foot = [x, y]

			else: #If there is no person detected label positions as none
				L_foot = [None, None]
				R_foot = [None, None]

			feet = [L_foot, R_foot]
			big_array.append(feet)
		big_array = np.array(big_array)

		left_array = big_array[:,0] #Take left foot position per frame and seperate into x and y
		right_array = big_array[:,1] #Take right foot position per frame and seperate into x and y

		xl = left_array[:,0]
		yl = left_array[:,1]
		xr = right_array[:,0]
		yr = right_array[:,1]

		#Show and save trajectory over image
		fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
		ax.imshow(img)
		ax.plot(xl, yl, 'b')
		ax.plot(xr, yr, 'r')
		#plt.show()
		plt.savefig('Data/Trajectory_pictures/'+exp[eriment]+'/'+vid+'.png')
		plt.close('all')

		#Apply tfm to points and image
		right_array 	= np.array([right_array], dtype = ('float32'))
		left_array 		= np.array([left_array], dtype = ('float32'))

		tf_left_array 	= cv2.perspectiveTransform(left_array, tfm)
		tf_right_array 	= cv2.perspectiveTransform(right_array, tfm)

		warped 			= cv2.warpPerspective(img, tfm, (2000, 2000))

		#Remove zeroes from trajecotries and change to None
		xl 						= 	zero_not_hero(tf_left_array[0][:,0])
		yl 						= 	zero_not_hero(tf_left_array[0][:,1])
		xr 						= 	zero_not_hero(tf_right_array[0][:,0])
		yr 						= 	zero_not_hero(tf_right_array[0][:,1])
		tf_left_array[0][:,0]	=	xl
		tf_left_array[0][:,1]	=	yl
		tf_right_array[0][:,0]	=	xr
		tf_right_array[0][:,1]	=	yr

		#Show final transformed trajectory:
		fig, ax = plt.subplots() #Plot left and right foot trajectory in blue and red
		ax.plot(xl, yl, 'b')
		ax.plot(xr, yr, 'r')
		#plt.show()
		plt.savefig('Data/Transformed_trajectories/'+exp[eriment]+'/'+vid+'.png')
		plt.close('all')

		#Compile data into dictionary and save, have to change to list so read as numpy
		dictionary = {
			'tfm' 		: tfm.tolist(),
			'left'		: left_array.tolist(),
			'right'		: right_array.tolist(),
			'tf_left' 	: tf_left_array.tolist(),
			'tf_right'	: tf_right_array.tolist(),
		}

		json_name = 'Data/'+exp[eriment]+'/'+vid+'/'+vid+'_dict.json'
		with open(json_name, 'w') as json_file:
			json.dump(dictionary, json_file)

		printProgressBar(i + 1, length, prefix = exp[eriment], suffix = vid, length = 40)
exit()