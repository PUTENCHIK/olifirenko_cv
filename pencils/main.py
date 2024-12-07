import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def dist(p1, p2) -> float:
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def get_pencils_from_image(image) -> tuple:
    for_show = image.copy()
    pencils = 0
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 130, 0), (255, 255, 255))
    cutted = cv2.bitwise_and(image, image, mask=mask)
    cutted = cv2.morphologyEx(cutted,
                              cv2.MORPH_OPEN,
                              np.ones((10, 10), np.uint8),
                              iterations=2)
    
    cutted_gray = cv2.cvtColor(cutted, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cutted_gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100_000:
            _, triangle =  cv2.minEnclosingTriangle(contour)
            points = [(int(p[0, 0]), int(p[0, 1])) for p in triangle]
            ribs = [
                dist(points[0], points[1]),
                dist(points[1], points[2]),
                dist(points[0], points[2])
            ]

            limit = 0.1
            if (abs(ribs[0] / ribs[1] - 1) < limit and
                    abs(ribs[1] / ribs[2] - 1) < limit and
                    abs(ribs[0] / ribs[2] - 1) < limit):
                continue

            cv2.line(for_show, points[0], points[1], (0, 255, 255), 5)
            cv2.line(for_show, points[1], points[2], (0, 255, 255), 5)
            cv2.line(for_show, points[0], points[2], (0, 255, 255), 5)
            pencils += 1
    
    return for_show, pencils


def count_pencils(paths) -> dict:
    result = dict()

    for path in paths:
        image = cv2.imread(str(path))
        _, pencils = get_pencils_from_image(image)
        result[path.name] = pencils

    return result


path = Path(__file__).parent / "images/"
paths = [p for p in path.glob("*.jpg")]

result = count_pencils(paths)

print(f"Sum of pencils: {sum(result.values())}")
for key in result:
    print(f"In file '{key}' {result[key]} pencils")

origin_window = "Images"
cv2.namedWindow(origin_window, cv2.WINDOW_NORMAL)

index = 0

while True:
    p = paths[index]
    image = cv2.imread(str(p))
    for_show, pencils = get_pencils_from_image(image)
    cv2.putText(for_show,
                "'n' - next, 'p' - previous",
                (60, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 0, 255), 3)
    cv2.putText(for_show,
                f"Pencils: {pencils}",
                (60, 260),
                cv2.FONT_HERSHEY_SIMPLEX,
                4, (0, 0, 255), 5)

    cv2.imshow(origin_window, for_show)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('n'):
        index = index+1 if index < len(paths)-1 else 0
    elif key == ord('p'):
        index = index-1 if index > 0 else len(paths)-1

cv2.destroyAllWindows()
