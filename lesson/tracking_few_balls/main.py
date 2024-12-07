import cv2
import random


def guess_in_line(password, centers):    
    xs = sorted([[round(centers[color][0], 3), color] for color in centers])
    
    for right, color in zip(password, xs):
        if right != color[1]:
            return False
        
    return True


def guess_square(password, centers):
    srtd = sorted([[round(centers[color][1], 3), round(centers[color][0], 3), color] for color in centers])
    
    if (srtd[0][1] > srtd[1][1]):
        srtd[0], srtd[1] = srtd[1], srtd[0]
    
    if (srtd[2][1] > srtd[3][1]):
        srtd[2], srtd[3] = srtd[3], srtd[2]
        
    for right, color in zip(password, srtd):
        if right != color[2]:
            return False
    
    return True


window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

bound_colors = {
    "red": (20, 20, 240),
    "green": (20, 240, 20),
    "blue": (240, 20, 20),
    "orange": (100, 100, 240)
}
colors_info = {
    "red": {
        "lower": (165, 115, 119),
        "upper": (179, 242, 222),
    },
    "green": {
        "lower": (70, 139, 159),
        "upper": (81, 252, 245),
    },
    "blue": {
        "lower": (94, 203, 170),
        "upper": (98, 255, 220),
    },
    "orange": {
        "lower": (4, 83, 220),
        "upper": (12, 212, 255),
    }
}
# print(colors.keys())
colors = list(colors_info.keys())
random.shuffle(colors)
password = [colors[:2], colors[2:]]

while camera.isOpened():
    ret, frame = camera.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    centers = dict()
    
    for c, color in enumerate(colors):
    
        mask = cv2.inRange(hsv, colors_info[color]["lower"], colors_info[color]["upper"])
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            (x, y), r = cv2.minEnclosingCircle(c)
            x, y, r = int(x), int(y), int(r)
            if r > 10:
                cv2.circle(frame, (x, y), 5, bound_colors[color], -1)
                cv2.circle(frame, (x, y), r, bound_colors[color], 2)
                
                centers[color] = (x, y)
        
        if len(centers) == len(colors):
            # if guess_in_line(colors, centers):
            if guess_square(colors, centers):
                answer = "CORRECT"
                color_text = bound_colors["green"]
            else:
                answer = "WRONG"
                color_text = bound_colors["red"]
            
            cv2.putText(frame,
                        f"{colors}, {answer}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color_text)
    
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()