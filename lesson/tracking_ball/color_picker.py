import cv2

window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)


def on_mouse_callback(event, x, y, *params):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = [y, x]


cv2.setMouseCallback(window_name, on_mouse_callback)
position = []
limits = [[255, 0], [255, 0], [255, 0]]

while camera.isOpened():
    ret, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
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
        cv2.putText(frame, f"Color HSV = {pixel_hsv}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
        
        cv2.putText(frame, f"Limits = {limits}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
    
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()

print(limits)