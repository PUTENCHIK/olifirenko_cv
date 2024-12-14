import zmq
import cv2
import numpy as np
    

def supdate(value):
    global slimit
    slimit = value


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5555
socket.connect(f"tcp://192.168.0.100:{port}")

slimit = 65

window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.createTrackbar("S", window_name, slimit, 255, supdate)

while True:
    msg = socket.recv()
    orig = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    frame = orig.copy()
    frame_area = frame.shape[0] * frame.shape[1]
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, slimit, 0])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    thresh = cv2.bitwise_and(frame, frame, mask=mask)
    
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(gray, slimit, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    amount = [0, 0]
    if len(contours):
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area / frame_area > 0.01:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int64(box)
                box_area = cv2.contourArea(box)
                if abs(area - box_area) / box_area < 0.18:
                    amount[0] += 1
                    color = (0, 255, 0)
                else:
                    amount[1] += 1
                    color = (0, 0, 255)
                
                cv2.drawContours(frame, [box], 0, (128, 128, 128), 2)
                cv2.drawContours(frame, contours, i, color, 2)
    
    cv2.putText(frame,
                f"Rects: {amount[0]}, circles: {amount[1]}",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 128, 0),
                2)
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('s'):
        cv2.imwrite("screen.png", orig)

cv2.destroyAllWindows()
