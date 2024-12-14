import cv2
import numpy as np
from pathlib import Path


def supdate(value):
    global slimit
    slimit = value


slimit = 125
path = Path(__file__).parent
image = cv2.imread(path / "screen.png")

window_name = "Screen"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.createTrackbar("S", window_name, slimit, 255, supdate)
first = True

while True:
    frame = image.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(gray, slimit, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cntr_list = contours[0]
    
    rect = cv2.minAreaRect(cntr_list)
    box = cv2.boxPoints(rect)
    box = np.int64(box)
    cv2.drawContours(frame, [box], 0, (255, 0, 255), 1)
    if first:
        print(box)
        first = False
    
    vx, vy, x, y = cv2.fitLine(cntr_list, cv2.DIST_L2, 0, 0.01, 0.01)
    lefty = int((-x * vy / vx) + y)
    righty = int((frame.shape[0] - x) * vy / vx + y)
    cv2.line(frame, (image.shape[0]-1, righty), (0, lefty), (0, 0, 128), 2)
    
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
