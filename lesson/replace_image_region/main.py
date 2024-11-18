import cv2
import numpy as np
from pathlib import Path


path = Path(__file__).parent
news = cv2.imread(path/ "news.jpg")
chebu = cv2.imread(path/ "cheburashka.jpg")

dest_pts = np.float32([[17, 25], [432, 55], [433, 269], [40, 294]])
src_pts = np.float32([[0, 0],
                      [chebu.shape[1], 0],
                      [chebu.shape[1], chebu.shape[0]],
                      [0, chebu.shape[0]]
])

M = cv2.getPerspectiveTransform(src_pts, dest_pts)
persp_img = cv2.warpPerspective(chebu, M, news.shape[:2][::-1])

gray = cv2.cvtColor(persp_img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
bg = cv2.bitwise_and(news, news, mask=cv2.bitwise_not(mask))
fg = cv2.bitwise_and(persp_img, persp_img, mask=mask)

result = cv2.add(bg, fg)

camera_name = "image"
cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(camera_name, result)
cv2.waitKey()
cv2.destroyAllWindows()
