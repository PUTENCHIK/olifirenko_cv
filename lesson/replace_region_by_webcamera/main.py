import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def get_camera_shape(camera) -> tuple:
    ret, frame = camera.read()
    return frame.shape


window_name = "No TV"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)
path = Path(__file__).parent
news = cv2.imread(path/ "news.jpg")

dest_pts = np.float32([[17, 25], [432, 55], [433, 269], [40, 294]])
camera_shape = get_camera_shape(camera)
src_pts = np.float32([[0, 0],
                      [camera_shape[1], 0],
                      [camera_shape[1], camera_shape[0]],
                      [0, camera_shape[0]]
])
M = cv2.getPerspectiveTransform(src_pts, dest_pts)

while camera.isOpened():
    ret, frame = camera.read()
    persp_img = cv2.warpPerspective(frame, M, news.shape[:2][::-1])
    
    gray = cv2.cvtColor(persp_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    bg = cv2.bitwise_and(news, news, mask=cv2.bitwise_not(mask))
    fg = cv2.bitwise_and(persp_img, persp_img, mask=mask)
    
    result = cv2.add(bg, fg)
    cv2.imshow(window_name, result)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()