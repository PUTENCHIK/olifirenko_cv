import cv2
import numpy as np


path = "https://cloud.iszf.irk.ru/index.php/s/ukRhcQNVViq5LH6/download"
video = cv2.VideoCapture(path)

limit = 25630
delta = 0.03
amount = 0
index = 1

while video.isOpened():
    _, frame = video.read()
    if frame is None:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 248, 0])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, np.ones((2, 2)))
    result = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    s = binary.sum() // 255

    if s >= limit * (1 - delta) and s <= limit * (1 + delta):
        print(index, end=' ')
        amount += 1
    index += 1

print()
print(f"Amount: {amount}")

video.release()
cv2.destroyAllWindows()
