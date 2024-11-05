import numpy as np
from skimage.measure import euler_number as eul_num, label


def ready_euler_number(image, conn: int) -> tuple:
    image = np.pad(image, 1)
    en = eul_num(image, connectivity=conn)
    amount = label(image, connectivity=conn).max()
    holes = amount - en

    return en, amount, holes


def invert_binary(b):
    return np.logical_not(b)


def my_euler_number(image, conn: int) -> tuple:
    image = np.pad(image, 1)
    amount = label(image, connectivity=conn).max()
    inverted = invert_binary(image)
    holes = label(inverted, connectivity=(2 if conn == 1 else 1)).max() - 1

    return amount - holes, amount, holes
