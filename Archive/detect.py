import cv2
import numpy as np
from matplotlib import pyplot as plt

temp = cv2.imread('template.jpg')
temp = temp.astype('uint8')
temp = cv2.cvtColor(temp, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
query = cv2.imread('control1frame1.jpg')
query = cv2.cvtColor(query, cv2.COLOR_RGB2BGR)


#Initiate SIFT
sift = cv2.xfeatures2d.SIFT_create()

#Find Keypoints
temp_kp, descriptors_temp = sift.detectAndCompute(temp, None)
query_kp, descriptors_query = sift.detectAndCompute(query, None)

#Run stuff
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors_temp, descriptors_query, 2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

MIN_MATCH_COUNT = 20

if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([temp_kp [m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([query_kp [m.trainIdx].pt for m in good]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h, w = temp.shape[:-1]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts, M)

    query = cv2.polylines(query,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

#Make lines
draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

#Draw the lines
img3 = cv2.drawMatches(temp, temp_kp, query, query_kp, good, None, **draw_params)
plt.imshow(img3)
plt.axis('off')
plt.show()


