import cv2 as cv
img = cv.imread("./happy.avif")

cv.imshow("Image", img)
k = cv.waitKey(0)