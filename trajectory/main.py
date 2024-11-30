import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from pathlib import Path
from pprint import pprint


def dist(p1: tuple, p2: tuple) -> float:
    y1, x1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def find_nearest(center: tuple, regions) -> tuple:
    minn = 1e6
    nearest = None
    # print(f"center: {center}")
    for region in regions:
        d = dist(center, region.centroid)
        # print(f"{i+1}) {region.centroid}: {d}")
        if d < minn:
            minn = d
            nearest = region.centroid
    
    # print()
    return nearest


path = Path(__file__).parent / "motion/"
files = sorted([str(file) for file in path.glob("*.npy")])
images = [np.load(file).astype(int) for file in files]

trajectories = list()

for index, frame in enumerate(images):
    labeled = label(frame)
    regions = regionprops(labeled)

    if len(trajectories) == 0:
        for region in regions:
            cy, cx = region.centroid
            trajectories += [[(float(cx), float(cy))]]
    else:
        for i, obj_trajectory in enumerate(trajectories):
            last_center = obj_trajectory[-1]
            ny, nx = find_nearest(last_center, regions)

            trajectories[i] += [(float(nx), float(ny))]


trajectories = np.array(trajectories)
# print(trajectories)

# for i, trajectory in enumerate(trajectories):
#     if (i == 0):
#         print(trajectory)
#         # plt.scatter(trajectory[:, 0], trajectory[:, 1], label=f"{i+1}")
#         plt.plot(trajectory[:, 0], trajectory[:, 1], label=f"{i+1}")

# plt.legend()
# plt.xlabel("x")
# plt.ylabel("y")
# plt.show()

# n = 4
# trajectory = trajectories[0]
# print(trajectory)
# diffs = np.abs(trajectory[1:] - trajectory[:-1])
# plt.plot(diffs, 'o')
# plt.show()

n = 16
# print(trajectories[0, 42:46])
for i in range(n):
    plt.subplot(4, 4, i+1)
    plt.title(i)
    plt.imshow(images[i])

plt.show()
