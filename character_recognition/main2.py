import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pprint import pprint


def recognize(region):
    if region.image.mean() == 1.0:
        return '-'
    en = euler_number(region.image)
    if en == -1:        # 8 or B
        left_half = region.image[:, :region.image.shape[1]//2]
        have_vl = np.sum(np.mean(left_half, axis=0) == 1) > 3
        if have_vl:
            return 'B'
        else:
            return '8'
    elif en == 0:       # A or 0
        image = region.image.copy()
        image[-1, :] = 1
        en = euler_number(image)
        if en == -1:
            return 'A'
        else:
            return '0'
        # cx, cy = region.local_centroid
        # cy /= region.image.shape[0]
        # cx /= region.image.shape[1]
        # return f"{cx}, {cy}"
    else:               # /, W, X, *, 1
        have_vl = np.sum(np.mean(region.image, axis=0) == 1) > 3
        if have_vl:
            return '1'
        else:
            if region.eccentricity < 0.4:
                return '*'
            else:
                image = region.image.copy()
                image = np.pad(image, pad_width=1, mode='maximum')
                en = euler_number(image)
                if en == -1:
                    return '/'
                elif en == -3:
                    return 'X'
                else:
                    return 'W'
    
    return None


image = plt.imread("character_recognition/alphabet.png")[:, :, :3].mean(2)
image[image > 0] = 1
image_labeled = label(image)
result = defaultdict(lambda: 0)

regions = regionprops(image_labeled)
for i, region in enumerate(regions):
    symbol = recognize(region)
    print(f"{i}) {symbol}")
    result[symbol] += 1

pprint(result)
# plt.imshow(image)
# plt.show()