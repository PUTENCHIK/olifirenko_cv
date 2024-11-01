from time import time
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label as ski_label


def show_figures(images):
    ln = len(images) if len(images) % 2 == 0 else len(images) + 1
    
    rows = int(ln ** 0.5)
    columns = ln // rows
    
    for i, (image, label, amount) in enumerate(images):
        plt.subplot(rows, columns, i+1)
        plt.title(f"label: {label}, amount: {amount}")
        plt.imshow(image)

    plt.show()


def bin_figure(LB, label, coords: tuple[tuple, tuple]):
    ys, xs = coords
    figure = LB[ys[0]:ys[1]+1, xs[0]:xs[1]+1]   # == label
    figure[figure == label] = 1

    return figure


def get_figure(LB, label) -> tuple:
    figure = LB == label
    whr = np.where(figure)
    ys = (int(whr[0].min()), int(whr[0].max()))
    xs = (int(whr[1].min()), int(whr[1].max()))

    return LB[ys[0]:ys[1]+1, xs[0]:xs[1]+1], (ys, xs)


def are_same(coords1, coords2) -> bool:
    ys1, xs1 = coords1
    ys2, xs2 = coords2
    return ys1[1] - ys1[0] == ys2[1] - ys2[0] and xs1[1] - xs1[0] == xs2[1] - xs2[0]


def find_figures(LB) -> dict:
    figures = []
    lbl = np.max(LB)
    for label in range(1, lbl+1):
        _, coords = get_figure(LB, label)
        figures += [coords]

    n = len(figures)
    unions = np.full(n, -1, dtype=int)
    for i, coords in enumerate(figures):
        if unions[i] != -1:
            continue

        if i < n-1:
            figure_i = bin_figure(LB, i+1, coords)
            for j in range(i+1, n):
                figure_j = bin_figure(LB, j+1, figures[j])
                if are_same(coords, figures[j]) and np.all(figure_i == figure_j):
                    unions[j] = i

    # arr = figures
    # for i, coords in enumerate(arr):
    #     ys, xs = coords
    #     figure = LB[ys[0]:ys[1] + 1, xs[0]:xs[1] + 1]
    #
    #     plt.subplot(2, 12, i+1)
    #     plt.imshow(figure)
    #     plt.title(f"{i+1}) {'unique' if unions[i] == -1 else unions[i]+1}")

    result = dict()
    for i, union in enumerate(unions):
        if union == -1:
            result[i+1] = 1
        else:
            result[union+1] += 1

    return result


image = np.load("figures/ps.npy.txt")#[896:971, 491:590]
labeled = ski_label(image)

print(f"Количество фигур: {np.max(labeled)}")

start = time()
result = find_figures(labeled.copy())
print(f"{round(time() - start, 3)} сек")
pprint(result)

images = []
for key in result:
    figure, _ = get_figure(labeled, key)
    images += [(figure, key, result[key])]

# show_images([image, labeled])
show_figures(images)
