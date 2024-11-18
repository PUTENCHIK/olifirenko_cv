import numpy as np
import cv2
import matplotlib.pyplot as plt


camera_name = "Camera"
cv2.namedWindow(camera_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read()
    cv2.imshow(camera_name, frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()