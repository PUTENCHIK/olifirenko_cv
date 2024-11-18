import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from pathlib import Path


def area(LB, label=1):
    return np.sum(LB == label)


path = Path(__file__).parent
B = np.load(path/ "coins.npy")
B = label(B)

nominals = [1, 2, 5, 10]
areas = {}
for i in range(1, np.max(B)+1):
    ar = int(area(B, i))
    if ar not in areas:
        areas[ar] = 1
    else:
        areas[ar] += 1

s = sum([nominals[i] * areas[key] for i, key in enumerate(sorted(areas))])

plt.imshow(B)
plt.title(f"Sum = {s}")
plt.show()