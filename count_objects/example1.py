import cv2
import numpy as np


image = cv2.imread("count_objects/arrow.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
arrow = contours[0]

cv2.drawContours(image, contours, 0, (0, 255, 0), 1)

print(f"Area = {cv2.contourArea(arrow)}")
print(f"Perimeter = {cv2.arcLength(arrow, False)}")

moments = cv2.moments(arrow)
# print(moments)
centroid = (int(moments['m10'] / moments['m00']),
            int(moments['m01'] / moments['m00']))
cv2.circle(image, centroid, 3, (0, 255, 0), 4)

eps = 1e-3 * cv2.arcLength(arrow, True)
approx = cv2.approxPolyDP(arrow, eps, True)
for p in approx:
    cv2.circle(image, tuple(*p), 2, (255, 0, 0), 2)
    
hull = cv2.convexHull(arrow)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i-1]), tuple(*hull[i]), (255, 0, 255), 1)
cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (255, 0, 255), 1)

x, y, w, h = cv2.boundingRect(arrow)
cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)

rect = cv2.minAreaRect(arrow)
box = cv2.boxPoints(rect)
box = np.int64(box)
cv2.drawContours(image, [box], 0, (255, 255, 0), 2)

(x, y), r = cv2.minEnclosingCircle(arrow)
center = int(x), int(y)
r = int(r)
cv2.circle(image, center, r, (128, 128, 128), 2)

ellipse = cv2.fitEllipse(arrow)
cv2.ellipse(image, ellipse, (0, 128, 0), 2)

vx, vy, x, y = cv2.fitLine(arrow, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x * vy / vx) + y)
righty = int((image.shape[0] - x) * vy / vx + y)
cv2.line(image, (image.shape[0]-1, righty), (0, lefty), (0, 0, 128), 2)

window_name = "Window"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
