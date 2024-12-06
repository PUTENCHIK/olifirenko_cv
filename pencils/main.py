import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


path = Path(__file__).parent / "images/"
files = sorted([str(file) for file in path.glob("*.jpg")])
images = [cv2.imread(file) for file in files]

print(images[0].shape)

result_window = "Result"
cv2.namedWindow(result_window, cv2.WINDOW_NORMAL)
origin_window = "Origin"
cv2.namedWindow(origin_window, cv2.WINDOW_NORMAL)

index = 0

while True:
    image = images[index]
    for_show = image.copy()
    cv2.putText(for_show,
                f"index = {index}",
                (80, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                4, (0, 0, 255), 4)
    
    hsv = cv2.cvtColor(images[index].copy(), cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([150, 150, 190])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    binary = result.mean(axis=2)
    inverted = np.zeros_like(binary)
    inverted[binary == 0] = 1
    
    cv2.imshow(origin_window, for_show)
    cv2.imshow(result_window, inverted)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('n'):
        index = index+1 if index < len(images)-1 else 0
        print(index, end=' ')
    elif key == ord('p'):
        index = index-1 if index > 0 else len(images)-1
        print(index, end=' ')

cv2.destroyAllWindows()
