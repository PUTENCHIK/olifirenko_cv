import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, sobel
from skimage.measure import label, regionprops


def fill(binary):
    result = binary.copy()
    for y in range(binary.shape[0]):
        flag = False
        for x in range(binary.shape[1]):
            if binary[y, x] == 1 and binary[y, x-1] == 0:
                flag = True
                print("to True:", y, x)
            if binary[y, x] == 0 and binary[y, x-1] == 1:
                flag = False
                print("to False:", y, x)
            if flag:
                result[y, x] = 1
    return result


image = plt.imread("lesson/lama_on_moon.png")[80:-40, 60:-40]

gray = np.mean(image, axis=2)
conts = sobel(gray)
thresh  = threshold_otsu(conts)
binary = conts > thresh
labeled = label(binary)
for region in regionprops(labeled):
    if region.area < 200 or region.perimeter < 1000:
        binary[np.where(labeled == region.label)] = 0
    

plt.title(f"{threshold_otsu(image)}")
plt.imshow(fill(binary), cmap="gray")
plt.show()
