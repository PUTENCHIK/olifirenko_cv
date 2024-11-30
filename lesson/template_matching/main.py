import cv2
import numpy as np
import matplotlib.pyplot as plt


window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
roi_name = "ROI"
cv2.namedWindow(roi_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

roi = None
while camera.isOpened():
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if roi is not None:
        corr_image = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        # cv2.imshow("Corr", corr_image)
        mib_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corr_image)
        top_left = max_loc
        bottom_right = (top_left[0] + roi.shape[1],
                        top_left[1] + roi.shape[0])
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0))
    
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        result = cv2.selectROI("ROI selection", gray)
        if result[1] != result[3] and result[0] != result[2]:
            roi = gray[int(result[1]):int(result[1] + result[3]),
                    int(result[0]):int(result[0] + result[2]),]
            cv2.imshow(roi_name, roi)
        cv2.destroyWindow("ROI selection")
    
camera.release()
cv2.destroyAllWindows()