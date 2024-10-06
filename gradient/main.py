import numpy as np
import matplotlib.pyplot as plt


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


def straight(size = 100, 
             color1 = [255, 0, 0], 
             color2 = [0, 0, 255]
    ):
    image = np.zeros((size, size, 3), dtype="uint8")
    assert image.shape[0] == image.shape[1]

    lin_space = np.linspace(0, 1, image.shape[0])

    for i, v in enumerate(lin_space):
        r = lerp(color1[0], color2[0], v)
        g = lerp(color1[1], color2[1], v)
        b = lerp(color1[2], color2[2], v)
        image[i, :, :] = [r, g, b]

    return image


def inclined(size = 100, 
             color1 = [255, 0, 0], 
             color2 = [0, 0, 255]
    ):
    image = np.zeros((size, size, 3), dtype="uint8")
    assert image.shape[0] == image.shape[1]

    lin_space = np.linspace(0, 1, 2*image.shape[0]-1)
    pixels = []

    for _, v in enumerate(lin_space):
        r = lerp(color1[0], color2[0], v)
        g = lerp(color1[1], color2[1], v)
        b = lerp(color1[2], color2[2], v)
        pixels += [[r, g, b]]
        
    for i in range(image.shape[0]):
        image[i:, i] = pixels[2*i:image.shape[0]+i]
        image[i, i:] = pixels[2*i:image.shape[0]+i]

    return image

size = 100
color1 = [255, 0, 0]
color2 = [0, 0, 255]

image1 = straight(size, color1, color2)
image2 = inclined(size, color1, color2)

plt.subplot(121)
plt.title("Сверху вниз")
plt.imshow(image1)

plt.subplot(122)
plt.title("По диагонали")
plt.imshow(image2)

plt.show()
