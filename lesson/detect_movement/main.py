import cv2
import numpy as np
import matplotlib.pyplot as plt


window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
bg_name = "Background"
cv2.namedWindow(bg_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_EXPOSURE, 10)

background = None
while camera.isOpened():
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)    

    if background is not None:
        delta = cv2.absdiff(background, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1500:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow(bg_name, thresh)
        
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('b'):
        background = gray.copy()
    
camera.release()
cv2.destroyAllWindows()