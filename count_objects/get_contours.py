import cv2
import numpy as np


def fupdate(value):
    global flimit
    flimit = value
    

def supdate(value):
    global slimit
    slimit = value


flimit = 100
slimit = 200

camera_name = "Camera"
cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
camera = cv2.VideoCapture(0)

cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
cv2.createTrackbar("S", "Mask", slimit, 255, supdate)

while camera.isOpened():
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    ctrs = cv2.Canny(gray, flimit, slimit)
    contours, _ = cv2.findContours(ctrs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        cv2.drawContours(frame, contours, i, (0, 0, 128), 3)
    
    cv2.imshow(camera_name, frame)
    cv2.imshow("Mask", ctrs)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()
