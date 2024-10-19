import matplotlib.pyplot as plt
import numpy as np


def dilation(B, struct):
    result = np.zeros_like(B)
    for y in range(1, B.shape[0]-1):
        for x in range(1, B.shape[1]-1):
            if B[y, x] == 1:
                result[y-1:y+2, x-1:x+2] = np.logical_or(B[y-1:y+2, x-1:x+2], struct)

    return result


def errosion(B, struct):
    result = np.zeros_like(B)
    for y in range(1, B.shape[0]-1):
        for x in range(1, B.shape[1]-1):
            sub = B[y-1:y+2, x-1:x+2]
            if np.all(sub == struct):
                result[y, x] = 1

    return result


def opening(B, struct):
    return dilation(errosion(B, struct), struct)


def closing(B, struct):
    return errosion(dilation(B, struct), struct)


struct = np.ones((3, 3))
# struct = np.array([[0, 1, 0],
#                    [1, 1, 1],
#                    [0, 1, 0],])

image = np.load("lesson/morph-array.npy")
plt.subplot(231)
plt.imshow(image)

plt.subplot(232)
plt.imshow(dilation(image, struct))

plt.subplot(233)
plt.imshow(errosion(image, struct))

plt.subplot(234)
plt.imshow(opening(image, struct))

plt.subplot(235)
plt.imshow(closing(image, struct))
plt.show()