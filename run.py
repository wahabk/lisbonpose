from lisbonpose.lisbonpose import Lisbon
import cv2

lisbon = Lisbon()

vidpath = 'Data/Videos/PA_02_LAC_13.mp4'
image = lisbon.getFrame(vidpath)
#image = image[800:1080, 900:1420]
image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 

corners = lisbon.detect_chess(image)
square = lisbon.draw_chess(image, corners)

cv2.imshow('drawn chess', square)
cv2.waitKey()

tfm = lisbon.get_tfm(image, corners)

warped = cv2.warpPerspective(square, tfm, (8000, 6000)) #This bit crops around rectangle
warped = cv2.resize(warped, (0,0), fx=0.1, fy=0.1) 

cv2.imshow('drawn chess', warped)
cv2.waitKey()

#apply tfm to points
#draw points on image
#show both transformed together
#find a way to do to all

