import mss
import pyautogui

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from time import sleep

from Config import Config


def stop_program():
    quit()


def preparing():
    if Config.START_PAUSE:
        sleep(Config.START_PAUSE)
    
    if Config.AUTO_ALT_TAB:
        pyautogui.hotkey('alt', 'tab')


def demonstrate(sct):
    window_name = "Screen"
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        screen = np.array(sct.grab(sct.monitors[0]))
        cv2.imshow(window_name, screen)

        key = cv2.waitKey(1)
        if key == ord(Config.KEY_QUIT_OPENCV):
            break


path = Path(__file__).parent

if __name__ == "__main__":
    
    # image = open()
    image = plt.imread(path / "templates/trex.png")
    plt.imshow(image)
    plt.show()

    # preparing()

    # with mss.mss() as sct:
        # demonstrate(sct)
        # pass
