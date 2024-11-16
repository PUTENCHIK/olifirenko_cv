import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, sobel
from skimage.measure import label, regionprops
from skimage.segmentation import flood_fill


image = plt.imread("lesson/lama_on_moon.png")[80:-40, 60:-40]

gray = np.mean(image, axis=2)
conts = sobel(gray)
thresh  = threshold_otsu(conts)
binary = conts > thresh
labeled = label(binary)
for region in regionprops(labeled):
    if region.area < 200 or region.perimeter < 1000:
        binary[np.where(labeled == region.label)] = 0
    
new_labeled = label(binary)
regions = regionprops(new_labeled)

cy, cx = regions[0].centroid
new_binary = flood_fill(binary, (int(cy), int(cx)), 1)

binary = conts > thresh

plt.imshow(new_binary * binary, cmap="gray")
plt.show()
