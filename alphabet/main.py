import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from skimage.morphology import closing
from collections import defaultdict
from pprint import pprint
from pathlib import Path


def recognize(region):
    if region.image.mean() == 1.0:
        return '-'
    image = closing(region.image.copy(), np.array([[1, 1], [1, 1]]))
    en = euler_number(image, 1)
    if en == -1:        # 8 or B
        left_half = region.image[:, :region.image.shape[1]//2]
        have_vl = np.sum(np.mean(left_half, axis=0) == 1) > 3
        if have_vl:
            return 'B'
        else:
            return '8'
    elif en == 0:       # A, 0, D, P
        image = region.image.copy()
        image[-1, :] = 1
        en = euler_number(image)
        if en == -1:
            return 'A'
        else:
            have_vl = np.sum(np.mean(region.image, axis=0) == 1) > 3
            if not have_vl:
                return '0'
            else:
                cy, cx = region.local_centroid
                cy /= region.image.shape[0]
                cx /= region.image.shape[1]
                # return f"{cy}, {cx}"
                if abs(cy - 0.5) > 0.08:
                    return 'P'
                else:
                    return 'D'
    else:               # /, W, X, *, 1
        have_vl = np.sum(np.mean(region.image, axis=0) == 1) > 3
        if have_vl:
            return '1'
        else:
            if region.eccentricity < 0.45:
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
                    print(region.eccentricity)
                    return 'W'
    
    return None


image = plt.imread("alphabet/symbols.png").mean(2)
image[image > 0] = 1
image_labeled = label(image)

result = defaultdict(lambda: 0)
regions = regionprops(image_labeled)

# path = Path("alphabet/images")
# path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate(regions):
    symbol = recognize(region)
    result[symbol] += 1

    # Сохранение символов
    # print(f"{i}) {symbol}")
    # plt.cla()
    # plt.title(f"Symbol - {symbol}")
    # plt.imshow(region.image)
    # plt.savefig(path/ f"image_{i:03d}.png")

pprint(result)
