import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import dilation, erosion, opening, closing
from collections import defaultdict


def show_images(images):
    l = len(images) if len(images)%2 == 0 else len(images)+1
    
    rows = int(l**0.5)
    columns = l // rows
    
    for i,image in enumerate(images):
        plt.subplot(rows, columns, i+1)
        plt.title(str(i+1))
        plt.imshow(image)

    plt.show()



figures = [[[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],],
           [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],],
           [[1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],],
           [[1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1],],
           [[1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1],],
]

image = np.load("figures/ps.npy.txt")[75:282, 1630:1842]
ims = [image]

obj = dict()
for i, figure in enumerate(figures):
    f = np.array(figure)
    cutted = closing(image, f)
    ims += [cutted]
    
    obj[str(figure)] = int(np.max(label(cutted)))

for key in obj:
    print(f"{key}: {obj[key]}")
show_images(ims)
