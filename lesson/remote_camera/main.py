import zmq
import cv2
import numpy as np


def on_mouse_callback(event, x, y, *params):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = [y, x]
        # pass


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5555
socket.connect(f"tcp://192.168.0.100:{port}")

window_name = "client"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.setMouseCallback(window_name, on_mouse_callback)
position = []

background = {
    "lower": (0, 4, 0),
    "upper": (255, 50, 255),
}

limits = [[255, 0], [255, 0], [255, 0]]

while True:
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, background["lower"], background["upper"])
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    if position:
        pixel_hsv = hsv[position[0], position[1]]
        for i,value in enumerate(pixel_hsv):
            if value < limits[i][0]:
                limits[i][0] = int(value)
            if value > limits[i][1]:
                limits[i][1] = int(value)

        cv2.circle(frame,
                   (position[1], position[0]),
                   5, (255, 255, 0), 2)
        # cv2.putText(frame, f"Color HSV = {pixel_hsv}", (10, 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
        cv2.putText(result, f"Limits = {limits}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
    
    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    elif key == ord('u'):
        limits = [[255, 0], [255, 0], [255, 0]]
    
    # cv2.putText(frame,
    #             f"Count: {count}",
    #             (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7, (255, 255, 0))
    # cv2.imshow(window_name, result)
    cv2.imshow(window_name, result)
    
cv2.destroyAllWindows()
