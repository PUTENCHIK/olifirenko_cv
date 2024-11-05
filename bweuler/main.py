import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

from bweuler import (
    ready_euler_number as ready_en,
    my_euler_number as my_en,
    invert_binary,
    images, file
)


def show_en(img, ngh: int = 4):
    if ngh not in (4, 8):
        raise Exception("Neighbours must be equal 4 or 8")

    img_pad = np.pad(img, 1)
    conn = 1 if ngh == 4 else 2

    en_r, f_r, d_r = ready_en(img_pad, conn)
    en_m, f_m, d_m = my_en(img_pad, conn)

    plt.title(
        f"Neighbours: {ngh}\n"
        f"Ready: euler_number = {f_r} - {d_r} = {en_r}\n"
        f"My: euler_number = {f_m} - {d_m} = {en_m}\n"
    )
    plt.axis('off')

    plt.subplot(1, 3, 1)
    plt.imshow(img_pad, cmap=plt.cm.gray)
    plt.title("Binary")

    plt.subplot(1, 3, 2)
    plt.imshow(label(img_pad, connectivity=conn))
    plt.title("Labeled")

    plt.subplot(1, 3, 3)
    plt.imshow(label(invert_binary(img_pad), connectivity=(2 if conn == 1 else 1)))
    plt.title("Inverted labeled")

    plt.show()


image = np.array(images[0])
show_en(image, 4)
