import numpy as np
import matplotlib.pyplot as plt


def neighbours(y, x):
    return ((y, x+1), (y, x-1), (y+1, x), (y-1, x))


def neighboursX(y, x):
    return ((y+1, x+1), (y-1, x-1), (y+1, x-1), (y-1, x+1))


def neighbours8(y, x):
    return neighbours(y, x) + neighboursX(y, x)


def area(LB, label=1):
    return np.sum(LB == label)


def centroid(LB, label=1):
    pos = np.where(LB == label)
    cy = np.mean(pos[0])
    cx = np.mean(pos[1])
    return cy, cx


def get_boundaries(LB, label=1, nbs=neighbours):
    pos = np.where(LB == label)
    bounds = []
    for y,x in zip(*pos):
        for yn, xn in nbs(y, x):
            if yn < 0 or yn > LB.shape[0]-1:
                bounds += [(y, x)]
                break
            elif xn < 0 or xn > LB.shape[1]-1:
                bounds += [(y, x)]
                break
            elif LB[yn, xn] != label:
                bounds += [(y, x)]
                break
    
    return bounds


def perimeter(LB, label=1, nbs=neighbours):
    return len(get_boundaries(LB, label, nbs))


def circularity(LB, label):
    return (float(perimeter(LB, label)**2 / area(LB, label)), 
            float(perimeter(LB, label, neighbours8)**2 / area(LB, label)))


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def circularity_std(LB, label=1, ngs=neighbours):
    r, c = centroid(LB, label)
    bounds = get_boundaries(LB, label, ngs)
    K = len(bounds)
    rd, sr = 0, 0
    
    for rk, ck in bounds:
        rd += distance((r, c), (rk, ck))
    rd /= K
    
    for rk, ck in bounds:
        sr += (distance((r, c), (rk, ck)) - rd)**2
    sr = (sr / K)**0.5
    
    return rd / sr


def draw_boundaries(LB, nbs=neighbours):
    BB = LB.copy()
    
    for label in range(1, int(np.max(BB))+1):
        bounds = get_boundaries(LB, label, nbs)
        print(circularity(LB, label))
        print(circularity_std(LB, label), circularity_std(LB, label, neighbours8))
        for y, x in bounds:
            BB[y, x] += 1
        
    return BB


def test_image():
    LB = np.zeros((16, 16), dtype="int")
    LB[4:, :4] = 2
    LB[3:10, 8:] = 1
    LB[[3, 4, 3], [8, 8, 9]] = 0
    LB[[8, 9, 9], [8, 8, 9]] = 0
    LB[[3, 4, 3], [-2, -1, -1]] = 0
    LB[[9, 8, 9], [-2, -1, -1]] = 0
    LB[12:-1, 6:9] = 3
    
    return LB


B = test_image()
plt.imshow(draw_boundaries(B))

# for label in range(1, int(np.max(B))+1):
#     print(perimeter(B, label))
    # y, x = centroid(B, label)
    # plt.scatter([x], [y])
    
plt.show()
