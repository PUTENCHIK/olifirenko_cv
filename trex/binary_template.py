import mss
import cv2
import pyautogui
import numpy as np
import keyboard
import time
import matplotlib.pyplot as plt
from pathlib import Path


def make_screenshots():
    last = None
    window_name = "Screen"
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    index = 1

    with mss.mss() as sct:
        while True:
            if keyboard.is_pressed('ctrl+shift+s'):
                screen = np.array(sct.grab(sct.monitors[0]))
                last = screen
                cv2.imwrite(f"templates/screen{index}.png", screen)
                index += 1
                time.sleep(2)
            if last is not None:
                cv2.imshow(window_name, last)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break


path = Path(__file__).parent / "templates/"
files = [file for file in path.glob("*.npy")]
images = [np.load(str(file)) for file in files]
# for i, image in enumerate(images):
#     image[image > 0.5] = 1
#     image[image < 1] = 0
#     new_image = np.zeros_like(image, dtype=int)
#     new_image[image == 0] = 1
#     images[i] = new_image

n = len(images)
for i, image in enumerate(images):
    # np.save(path / f"{files[i].stem}.npy", image)
    plt.subplot(1, n, i+1)
    plt.imshow(image)

plt.show()
