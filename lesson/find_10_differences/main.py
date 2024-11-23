import cv2
from pathlib import Path


path = Path(__file__).parent

cat = cv2.imread(path/ "cat.png")
cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread(path/ "cat2.png", cv2.IMREAD_GRAYSCALE)

diff = cv2.absdiff(cat1, cat2)
thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)

contours, hierarchy = cv2.findContours(thresh.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
cv2.putText(cat, f"Differences = {len(contours)}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (0, 0, 255))

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(cat, (x, y), (x+w, y+h), (0, 0, 255), 1)

cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.imshow("Original", cat)

cv2.namedWindow("Difference", cv2.WINDOW_NORMAL)
cv2.imshow("Difference", thresh)

key = cv2.waitKey()
cv2.destroyAllWindows()
