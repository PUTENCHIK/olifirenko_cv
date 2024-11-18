import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.draw import disk


def hist(gray):
    h = np.zeros(256)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            h[gray[i, j]] += 1

    return h


image = np.zeros((1000, 1000), dtype="uint8")
image[:] = np.random.randint(20, 75, size=image.shape)

rr, cc = disk((500, 500), 220)
image[rr, cc] = np.random.randint(60, 160, size=len(rr))

rr, cc = disk((800, 800), 200)
image[rr, cc] = np.random.randint(20, 120, size=len(rr))

plt.subplot(131)
plt.imshow(image)

plt.subplot(132)
plt.plot(hist(image))

B = image.copy()
l = 80
B[B < l] = 0
B[B > 0] = 1

plt.subplot(133)
plt.imshow(B)

plt.show()