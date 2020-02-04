from pathlib import Path
import json
from PIL import Image, ImageDraw
import time

start = time.time()

path = Path("/home/wahab/deep_learning/json")
keypoint_files = path.iterdir()

# image = Image.new('RGB', (1280, 960))
image = Image.open("/home/wahab/Data/pic.jpg")
drawer = ImageDraw.Draw(image, 'RGBA')

def read_keypoints(keypoint_filename):
	keypoint_file = keypoint_filename.open()
	keypoint_data = json.load(keypoint_file)
	keypoint_file.close()
	return keypoint_data

def find_pose_keypoints(keypoint_data):
	keypoints = keypoint_data['people']
	if (len(keypoints) >= 1):
		keypoints = keypoints[0]
		keypoints = keypoints['pose_keypoints_2d']
		return keypoints
	else:
		return []

class Keypoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def get_joint_keypoints(pose_keypoints):
	# list comp
	if (len(pose_keypoints) >= 1):	
		footL = create_keypoint(pose_keypoints, 19 * 3)
		footR = create_keypoint(pose_keypoints, 22 * 3)
		joint_keypoints = [footL, footR]
		return joint_keypoints
	else:
		return []

def create_keypoint(pose_keypoints, i):
	x = pose_keypoints[i]
	y = pose_keypoints[i+1]
	keypoint = Keypoint(x, y)
	return keypoint

def draw_keypoints(drawer, keypoints):
	for keypoint in keypoints:
		draw_keypoint(drawer, keypoint.x, keypoint.y, 10)

def draw_keypoint(drawer, x, y, s):
	x1 = x - s/2
	x2 = x + s/2
	y1 = y - s/2
	y2 = y + s/2
	# drawer.ellipse((x1, y1, x2, y2), (255, 0, 0, 32))
	# drawer.rectangle((x1, y1, x2, y2), (255, 0, 255, 255))
	drawer.ellipse((x1, y1, x2, y2), (255, 0, 255, 5))
	# drawer.ellipse((x1, y1, x2, y2), fill = (255, 0, 0, 32), outline = (0, 0, 0, 0))
	# drawer.point((x, y))


for keypoint_file in sorted(keypoint_files):
	print(keypoint_file)
	data = read_keypoints(keypoint_file)
	points = find_pose_keypoints(data)
	joints = get_joint_keypoints(points)
	draw_keypoints(drawer, joints)

image.show("hello")

end = time.time()
print(end - start)




