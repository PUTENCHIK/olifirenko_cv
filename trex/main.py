import mss
import pyautogui
import cv2
import numpy as np
import time

from pathlib import Path
from skimage.measure import label, regionprops
from skimage.morphology import erosion, dilation

from Config import Config


def stop_program():
    quit()


def screenshot(sct, monitor = None):
    return np.array(sct.grab(sct.monitors[0] if monitor is None else monitor))


def main_monitor(sct):
    return sct.monitors[0]


def add_padding(monitor, padd: int|list|dict):
    if isinstance(padd, dict):
        return {
            "top": monitor["top"] + padd["top"],
            "left": monitor["left"] + padd["left"],
            "width": monitor["width"] - padd["right"] - padd["left"],
            "height": monitor["height"] - padd["top"] - padd["bottom"],
        }
    elif isinstance(padd, int):
        return {
            "top": monitor["top"] + padd,
            "left": monitor["left"] + padd,
            "width": monitor["width"] - 2*padd,
            "height": monitor["height"] - 2*padd,
        }
    elif isinstance(padd, list):
        # top left bottom right
        return {
            "top": monitor["top"] + padd[0],
            "left": monitor["left"] + padd[1],
            "width": monitor["width"] - padd[1] - padd[3],
            "height": monitor["height"] - padd[0] - padd[2],
        }
    else:
        raise TypeError


def binary_frame(frame):
    frame = frame.copy().mean(2)
    # plt.imshow(frame)
    # plt.show()

    result = np.zeros_like(frame, dtype=int)

    mask1 = frame >= Config.trex_color_limits[0]
    mask2 = frame <= Config.trex_color_limits[1]
    mask = np.logical_and(mask1, mask2)

    result[mask] = 1

    return result


def find_game_area() -> tuple:
    monitor = main_monitor(sct)
    monitor = add_padding(monitor, Config.start_padding)

    screen = screenshot(sct, monitor)
    binary = binary_frame(screen)
    labeled = label(binary)
    regions = regionprops(labeled)

    trex = regions[0]
    max_x = 0
    for region in regions:
        if region.area > trex.area:
            trex = region
        if region.centroid[1] > max_x:
            max_x = region.centroid[1]

    y, x = trex.centroid
    ay, ax = int(y) + Config.start_padding[0], int(x) + Config.start_padding[1]
    h, w = trex.image.shape

    return (ax + w, ay - int(h*1.5), int(max_x) + Config.start_padding[1], ay + h), ay - int(h/2)


def get_sorted_xs(regions, monitor):
    # returns x and absolute y of regions, sorted by x
    xs = list()
    for region in regions:
        xs += [(
            int(region.centroid[1]),
            int(region.centroid[0] + monitor["top"] + region.image.shape[0]/2),
            region
        )]

    return sorted(xs)


def distance(p1, p2) -> float:
    y1, x1 = p1
    y2, x2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def preparing():
    if Config.START_PAUSE:
        time.sleep(Config.START_PAUSE)
    
    if Config.AUTO_ALT_TAB:
        pyautogui.hotkey('alt', 'tab')


def demonstrate(sct, frame = None):
    window_name = "Screen"
    window = cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    screen = frame

    while True:
        if frame is None:
            screen = screenshot(sct)

        cv2.imshow(window_name, screen)

        key = cv2.waitKey(1)
        if key == ord(Config.KEY_QUIT_OPENCV):
            break


path = Path(__file__).parent

if __name__ == "__main__":
    with mss.mss() as sct:
        preparing()

        (x1, y1, x2, y2), trex_y = find_game_area()
        width, height = x2 - x1, y2 - y1
        game_monitor = {"left": x1, "top": y1, "width": width, "height": height}
        pyautogui.press("space")

        ratio_for_jump = Config.default_ratio_for_jump
        delay_for_increase_ratio = Config.default_delay_for_increase_ratio
        timer = time.time()

        while True:
            screen = screenshot(sct, game_monitor)

            binary = erosion(binary_frame(screen), np.ones((2, 2), dtype=int))
            binary = dilation(binary, np.ones((5, 5), dtype=int))
            labeled = label(binary)
            regions = regionprops(labeled)

            if time.time() > timer + delay_for_increase_ratio:
                ratio_for_jump *= Config.factor_ratio_for_jump
                delay_for_increase_ratio *= Config.factor_delay_for_increase_ratio
                timer = time.time()

            if len(regions):
                srtd = get_sorted_xs(regions, game_monitor)
                coef_two_regions = 1
                if len(regions) > 1:
                    first, second = srtd[0][2], srtd[1][2]
                    dist = distance(first.centroid, second.centroid)
                    dist_normed = dist / width
                    coef_two_regions = 1 if dist_normed > 0.25 else 0.25 / dist_normed
                    # print(f"dist: {dist}, width: {width}, normed: {dist_normed}")

                x0, y0, _ = srtd[0]
                limit = ratio_for_jump * coef_two_regions
                if x0 / width < limit:
                    # print(limit, delay_for_increase_ratio)
                    if y0 > trex_y:
                        pyautogui.press("space")

            if pyautogui.position() == (0, 0):
                break
