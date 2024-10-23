from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import (
    binary_dilation,
    binary_erosion,
    binary_closing,
    binary_opening
)

def get_figures():
    return [
        np.array([[0, 0, 1, 0, 0],
                  [0, 0, 1, 0, 0],
                  [1, 1, 1, 1, 1],
                  [0, 0, 1, 0, 0],
                  [0, 0, 1, 0, 0],
        ]),
        np.array([[1, 0, 0, 0, 1],
                  [0, 1, 0, 1, 0],
                  [0, 0, 1, 0, 0],
                  [0, 1, 0, 1, 0],
                  [1, 0, 0, 0, 1],
        ]),
    ]


def count_objects(image):
    result = {
        'pluses': 0,
        'stars': 0,
    }
    masks = get_figures()

    for y in range(2, image.shape[0]-2):
        for x in range(2, image.shape[1]-2):
            sub = image[y-2:y+3, x-2:x+3]
            if np.all(sub == masks[0]):
                result['pluses'] += 1
            elif np.all(sub == masks[1]):
                result['stars'] += 1

    return result


image = np.load("stars/stars.npy").astype(int)
print(image.shape)
result = count_objects(image)

plt.imshow(image)
plt.title(f"stars: {result['stars']}, pluses: {result['pluses']}")
plt.show()