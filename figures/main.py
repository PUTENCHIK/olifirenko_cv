from time import time
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label as ski_label, regionprops


def show_figures(regions, obj):
    ln = len(obj) if len(obj) % 2 == 0 else len(obj) + 1
    
    rows = int(ln ** 0.5)
    columns = ln // rows
    
    for i, label in enumerate(obj):
        plt.subplot(rows, columns, i+1)
        plt.title(f"label: {label}, amount: {obj[label]}")
        plt.imshow(regions[label-1].image)

    plt.show()


def find_figures(regions) -> dict:
    figures = dict()
    for i, region in enumerate(regions):
        bin_image = region.image
        is_new = True
        for label in figures:
            bin_obj = regions[label-1].image
            if bin_image.shape == bin_obj.shape and np.all(bin_image == bin_obj):
                figures[label] += 1
                is_new = False
                break
        if is_new:
            figures[region.label] = 1

    return figures


image = np.load("figures/ps.npy.txt")
labeled = ski_label(image)
regions = regionprops(labeled)

print(f"Количество фигур: {np.max(labeled)}")

start = time()
result = find_figures(regions)
print(f"{round(time() - start, 3)} сек")
pprint(f"Фигуры: {result}")

show_figures(regions, result)
