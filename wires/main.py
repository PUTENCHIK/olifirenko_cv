from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import (
    binary_dilation,
    binary_erosion,
    binary_closing,
    binary_opening
)


import numpy as np
import matplotlib.pyplot as plt


def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)


def exist(B, nbs):
    left, top = nbs

    if left[0] >= 0 and left[0] <= B.shape[0] and left[1] >= 0 and left[1] < B.shape[1]:
        if B[left] == 0:
            left = None
    else:
        left = None


    if top[0] >= 0 and top[0] <= B.shape[0] and top[1] >= 0 and top[1] < B.shape[1]:
        if B[top] == 0:
            top = None
    else:
        top = None

    return left, top


def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]

    return j


def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)

    if j != k:
        linked[k] = j


def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="uint")
    label = 1

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)
                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)

                LB[y, x] = m

                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label

    uniques = np.unique(LB)[1:]

    for i, v in enumerate(uniques):
        LB[LB == v] = i + 1

    return LB, uniques.shape[0]


def cut_wire(image):
    result = {
        'wires': []
    }
    passed, amount = two_pass(image)

    for mark in range(1, amount+1):
        wire = passed == mark
        struct = np.array([[1],
                           [1],
                           [1],])

        wire = binary_erosion(wire, struct).astype(int)
        wire, cuts = two_pass(wire)
        match (cuts):
            case (0):
                status = 'fully destroyed'
            case 1:
                status = 'not damaged'
            case _:
                status = 'damaged'

        result['wires'] += [{
            'parts': cuts,
            'status': status
        }]

    return result


def cut_all(images):
    length = len(images)
    rows = int(length**0.5)
    columns = length // rows
    if rows * columns != len(images):
        columns += 1
    
    for i, image in enumerate(images):
        res = cut_wire(image)
        plt.subplot(rows, columns, i+1)
        title = "\n".join([f"{j+1}) parts: {wire['parts']}, status: {wire['status']}" for j, wire in enumerate(res['wires'])])
        plt.title(title)
        plt.imshow(image)

    plt.tight_layout()
    plt.show()


files = Path("wires/files/").glob("*.txt")
pathes = sorted([str(path) for path in files])
images = [np.load(path).astype(int) for path in pathes]

cut_all(images)
