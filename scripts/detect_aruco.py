import cv2
import lisbonpose


if __name__ == "__main__":
    img = cv2.imread("/home/wahab/code/lisbonpose/pics/floor.jpg", cv2.IMREAD_COLOR)

    cv2.imshow('image', img)
    cv2.waitKey()

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)


    print(corners) 