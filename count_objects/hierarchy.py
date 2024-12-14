import cv2
import numpy as np


image = cv2.imread("count_objects/hierarchy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(hierarchy)

for i in range(len(contours)):
    b = bin(i)
    cv2.drawContours(image, contours, i, (55 + 200 * (i & 0b100),
                                          55 + 200 * (i & 0b010),
                                          55 + 200 * (i & 0b001)), 3)
    c = contours[i][0][0]
    cv2.putText(image,
                f"{i}) {hierarchy[0][i]}",
                c,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3)

window_name = "Window"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
