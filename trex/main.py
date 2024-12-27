import mss
import cv2
import time
import pyautogui
import numpy as np
from pathlib import Path

from Config import Config


def stop_program():
    quit()


def screenshot(sct, monitor = None, padding: int = None):
    mon = sct.monitors[0] if monitor is None else monitor
    if padding is not None:
        mon['top'] += padding
        mon['left'] += padding
        mon['width'] -= 2*padding
        mon['height'] -= 2*padding

    return np.array(sct.grab(mon))


def main_monitor(sct):
    return sct.monitors[0]


def preparing():
    if Config.START_PAUSE:
        time.sleep(Config.START_PAUSE)


def to_binary(screen):
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, Config.trex_color_limits-1])
    upper = np.array([0, 0, Config.trex_color_limits+1])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, np.ones((2, 2), dtype=int))
    mask = cv2.dilate(mask, np.ones((2, 2), dtype=int))
    _, binary = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    return binary


def get_game_area(screen, binary):
    bounds = {
        'min_x': screen.shape[1],
        'min_y': screen.shape[0],
        'max_x': 0,
        'max_y': 0,
    }
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        if area > 15:
            # print(contour.shape)
            # cv2.rectangle(screen, (x, y), (x+w, y+h), (128, 0, 0), 1)
            if x+w < bounds['min_x']:
                bounds['min_x'] = x+w
            if x+w > bounds['max_x']:
                bounds['max_x'] = x+w
            if y+h < bounds['min_y']:
                bounds['min_y'] = y+h
            if y+h > bounds['max_y']:
                bounds['max_y'] = y+h

    if bounds['min_x'] == bounds['max_x']:
        bounds['max_x'] += Config.default_game_area_width
    if bounds['min_y'] == bounds['max_y']:
        bounds['max_y'] -= Config.default_game_area_height
    
    bounds['min_x'] += 20

    return bounds


def draw_game_area(screen, game_area):
    cv2.rectangle(screen,
                (game_area['min_x'], game_area['min_y']),
                (game_area['max_x'], game_area['max_y']), (0, 0, 128), 2)
    return screen


def distance(p1, p2) -> float:
    y1, x1 = p1
    y2, x2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def get_objects(screen):
    binary = to_binary(screen)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        dist = (x+w)//2

        objects += [dist]
    
    return sorted(objects)


path = Path(__file__).parent
debug_window = "Debug"
cv2.namedWindow(debug_window, cv2.WINDOW_GUI_NORMAL)


# def on_mouse_callback(event, x, y, *params):
#     global position
#     if event == cv2.EVENT_LBUTTONDOWN:
#         position = [y, x]

# position = None
# cv2.setMouseCallback(debug_window, on_mouse_callback)

if __name__ == "__main__":
    with mss.mss() as sct:
        preparing()
        screen = screenshot(sct, padding=Config.start_padding)
        binary = to_binary(screen)
        game_area = get_game_area(screen, binary)

        game_monitor = {
            "top": game_area['min_y'] + Config.start_padding,
            "left": game_area['min_x'] + Config.start_padding,
            "width": game_area['max_x'] - game_area['min_x'],
            "height": game_area['max_y'] - game_area['min_y'],
        }
        print(game_monitor)
        flag = True

        while True:
            screen = screenshot(sct)
            # screen = draw_game_area(screen, game_area)

            # if flag:
            #     objects = get_objects(screen)
            #     print(objects)
            #     flag = False
            
            # if position:
            #     hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            #     pixel = hsv[position[0], position[1]].astype(int)
            #     cv2.putText(screen,
            #                 f"{pixel}",
            #                 (30, 60),
            #                 cv2.FONT_HERSHEY_SIMPLEX,
            #                 0.7,
            #                 (0, 255, 0),
            #                 3)
            # binary = to_binary(screen)
            # mask = get_game_area(screen, binary)

            cv2.imshow(debug_window, screen)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            if pyautogui.position() == (0, 0):
                break

cv2.destroyAllWindows()
