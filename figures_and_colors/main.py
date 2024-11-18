from collections import defaultdict
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
from pathlib import Path


path = Path(__file__).parent
im = plt.imread(path/ "balls_and_rects.png")[:500, :500]

binary = im.copy().mean(2)
binary[binary > 0] = 1
labeled = label(binary)
regions = regionprops(labeled)
im_hsv = rgb2hsv(im)


def isRect(region) -> int:
    """
    If region.image is rectangle, returns 1, and 0 if is circle.
    """
    y, x = region.image.shape
    return int(x*y == region.area)


colors = defaultdict(lambda: [0, 0])
unique_colors = defaultdict(lambda: [0, 0])

for i, region in enumerate(regions):
    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]
    is_rect = isRect(region)
    
    unique_colors[float(color)][is_rect] += 1

    flag = True
    for clr in colors:
        if abs(color - clr) < 0.04:
            colors[float(clr)][is_rect] += 1
            flag = False
            break
    if flag:
        colors[float(color)][is_rect] = 1


pprint(unique_colors)
pprint(colors)

# plt.subplot(1, 2, 1)
# plt.imshow(im_hsv[:, :, 0] == 0.6111111044883728)
# plt.subplot(1, 2, 2)
# plt.imshow(im_hsv)
# plt.title(f"Figures: {len(regions)}")
# plt.show()
