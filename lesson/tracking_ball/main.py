import cv2
import time
import numpy as np


window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

lower = (59, 110, 110)
upper = (76, 255, 255)
D = 0.077
color_green = (20, 230, 20)
color_trajectory = np.array([128, 0, 255])

camera = cv2.VideoCapture(0)

trajectory = []
speeds = []
queue_len = 30

prev_time = time.time()
curr_time = time.time()
r = 1

while camera.isOpened():
    ret, frame = camera.read()
    curr_time = time.time()
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)    
    
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        x, y, r = int(x), int(y), int(r)
        trajectory += [((x), y)]
        if len(trajectory) > queue_len:
            trajectory.pop(0)
        if r > 10:
            cv2.circle(frame, (x, y), 5, color_green, -1)
            cv2.circle(frame, (x, y), r, color_green, 2)
            
        for i in range(1, len(trajectory)-1):
            cv2.line(frame,
                     trajectory[i-1],
                     trajectory[i],
                     (i / queue_len) * color_trajectory,
                     i//10+1)
        time_diff = curr_time - prev_time
        if len(trajectory) >= 2:
            x1, y1 = trajectory[-1]
            x2, y2 = trajectory[-2]
            dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
            pxl_per_mtr = D / 2 / r
            dist *= pxl_per_mtr
            speed = dist / time_diff
            speeds += [speed]
            if len(speeds) > queue_len:
                speeds.pop(0)
            
            cv2.putText(frame,
                        f"Speed: {speed:.3f}m/s, Avg: {(sum(speeds)/len(speeds)):.3f}m/s",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255))
            prev_time = curr_time
    
    cv2.imshow("Mask", mask)
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()