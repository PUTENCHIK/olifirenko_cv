import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from pathlib import Path
from pprint import pprint


def dist(p1: tuple, p2: tuple) -> float:
    y1, x1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def find_nearest(centers: tuple, regions, visited: list) -> tuple:
    minn = 1e6
    index = None
    for i, region in enumerate(regions):
        if i not in visited:
            dists = np.array([dist(center, region.centroid) for center in centers])
            if dists.mean() < minn:
                minn = dists.mean()
                index = i
    
    return regions[index].centroid, index
            


def plot_differencies(trajectory):
    diffs = np.abs(trajectory[1:] - trajectory[:-1])
    plt.plot(diffs, 'o')
    plt.show()


def show_images(trajectories, images):
    plt.ion()
    for i, image in enumerate(images):
        plt.clf()
        plt.title(i)
        plt.imshow(image)
        for j, trajectory in enumerate(trajectories):
            plt.scatter(trajectory[i][0],
                        trajectory[i][1],
                        c=['blue', 'red', 'green'][j],
                        s=3)
        
        plt.pause(1)


def plot_trajectories(trajectories):
    for i, trajectory in enumerate(trajectories):
        # plt.plot(trajectory[:, 0], trajectory[:, 1], label=f"{i+1}")
        plt.scatter(trajectory[:, 0], trajectory[:, 1], label=f"{i+1}")

    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


path = Path(__file__).parent / "motion/"
files = sorted([str(file) for file in path.glob("*.npy")])
images = [np.load(file).astype(int) for file in files]

trajectories = list()

for index, frame in enumerate(images):
    labeled = label(frame)
    regions = regionprops(labeled)
    visited = list()

    if len(trajectories) == 0:
        for region in regions:
            cy, cx = region.centroid
            trajectories += [[(float(cx), float(cy))]]
    else:
        for i, obj_trajectory in enumerate(trajectories):
            depth = 3
            last_centers = obj_trajectory[-depth:]
            (ny, nx), index = find_nearest(last_centers,
                                           regions,
                                           visited)

            trajectories[i] += [(float(nx), float(ny))]
            visited += [index]


trajectories = np.array(trajectories)

plot_trajectories(trajectories)
