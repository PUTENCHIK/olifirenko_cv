import cv2
import numpy as np
from pathlib import Path


path = Path(__file__).parent
image = cv2.imread(path/ "rose.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([0, 100, 100])
upper = np.array([1, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
mask = cv2.dilate(mask, np.ones((10, 10)))

result = cv2.bitwise_and(image, image, mask=mask)

camera_name = "image"
cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(camera_name, result)
cv2.waitKey()
cv2.destroyAllWindows()
