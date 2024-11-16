from collections import defaultdict
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv


im = plt.imread("lesson/balls.png")
binary = im.copy().mean(2)
binary[binary > 0] = 1
labeled = label(binary)
regions = regionprops(labeled)

im_hsv = rgb2hsv(im)

unique_colors = dict()
colors = []
for i, region in enumerate(regions):
    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]
    colors += [float(color)]

    flag = True
    for clr in unique_colors:
        if abs(color - clr) < 0.04:
            unique_colors[float(clr)] += 1
            flag = False
            break
    if flag:
        unique_colors[float(color)] = 1
    
pprint(unique_colors)

# plt.figure()
plt.title(f"Colors: {len(unique_colors)}")
plt.subplot(1, 3, 1)
plt.imshow(im)

plt.subplot(1, 3, 2)
plt.imshow(binary)

plt.subplot(1, 3, 3)
plt.plot(sorted(colors), 'o')

plt.show()