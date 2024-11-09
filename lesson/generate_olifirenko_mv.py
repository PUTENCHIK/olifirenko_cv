import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from skimage.morphology import closing
from collections import defaultdict
from pprint import pprint
from pathlib import Path


w, h = 640, 480
image = np.zeros((h, w, 3), dtype="uint8")

color1 = np.array([216, 0, 95])
color2 = np.array([135, 234, 0])

for p in np.linspace(0, 1, 20):
    color = color1 * (1 - p) + color2 * p
    start = int(image.shape[1] * p)
    end = int(image.shape[1] * (p+1))
    print(start, end)
    print(color)
    image[start:end, :, :] = np.array(color)

plt.imshow(image)
path = Path("lesson/")
plt.savefig(path/ f"olifirenko_mv.png")
