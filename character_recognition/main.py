import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from collections import defaultdict
from pprint import pprint
from pathlib import Path


def distance(v1, v2):
    return ((v1 - v2)**2).sum() ** 0.5


def extractor(region):
    area = np.sum(region.area) / region.image.size
    perimeter = region.perimeter / region.image.size
    cy, cx = region.local_centroid
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    eul = region.euler_number
    eccentricity = region.eccentricity
    have_vl = np.sum(np.mean(region.image, axis=0) == 1) > 3
    
    return np.array([area, perimeter, cy, cx, eul, eccentricity, have_vl])


def classificator(region, classes):
    det_class = None
    v = extractor(region)
    min_distanse = 1e10
    for cls in classes:
        dist = distance(v, classes[cls])
        if dist < min_distanse:
            min_distanse = dist
            det_class = cls
    
    return det_class


image = plt.imread("character_recognition/alphabet.png")[:, :, :3].mean(2)
image[image > 0] = 1
image_labeled = label(image)

template = plt.imread("character_recognition/alphabet-small.png")[:, :, :3].mean(2)
template[template < 1] = 0
template = np.logical_not(template)
template_labeled = label(template)

regions = regionprops(template_labeled)
classes = "80AB1WX*/-"
extractors = dict()
for cls, rgn in zip(classes, regions):
    extractors[cls] = extractor(rgn)

classes = extractors

plt.figure()
for i, cls in enumerate(classes):
    plt.subplot(2, 5, i+1)
    plt.title(f"{i}) {classes[cls]}")
    plt.imshow(regions[i].image)

symbols = defaultdict(lambda: 0)
path = Path("character_recognition/images")
path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate(regionprops(image_labeled)):
    # print(region.label, end=" ")
    symbol = classificator(region, classes)
    symbols[symbol] += 1
    
    plt.cla()
    plt.title(f"Symbol - {symbol}, {region.euler_number}")
    plt.imshow(region.image)
    plt.savefig(path/ f"image_{i:03d}.png")
    
print()
pprint(symbols)

# plt.show()