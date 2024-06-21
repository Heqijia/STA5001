import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from tqdm import tqdm

def points_within_distance(point, n,p):
    x, y = point
    flag=1
    points = []
    for i in range(x - p, x + p + 1):
        for j in range(y - p, y + p + 1):
            if (i != x or j != y) and manhattan_pro(point, (i, j), n) <= p:
                if i<0:
                    flag=0
                if j<0:
                    flag=0
                if i>=n:
                    flag=0
                if j>=n:
                    flag=0
                if flag==1:
                    points.append([i, j])
                else:
                    flag=1
    return points

def points_in_distance(point, n, dist):
    x, y = point
    candidates=[[x-dist,y],[x, y+dist],[x+dist,y],[x, y-dist]]
    candidates_2=[]
    for i in range(len(candidates)):
        if candidates[i][0]<0:
            continue
        if candidates[i][1]<0:
            continue
        if candidates[i][0]>=n:
            continue
        if candidates[i][1]>=n:
            continue
        candidates_2.append(candidates[i])
    return candidates_2


"""poiint_i=(a1,b1), point_j=(a2,b2), n is the size of the network"""
def manhattan_pro(point_i, point_j, n):
    x1, y1 = point_i
    x2, y2 = point_j
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    # dx = min(dx, n - dx)  
    # dy = min(dy, n - dy) 
    return dx + dy

"""Generate the distribution array for the long range connection"""
def generate_distribution_array(n,p,r):
    dist=n
    distribution=[]
    distance=[]
    for i in range(p+1, dist+1):
        distribution.append(1/(i)**r)
        distance.append(i)
    distribution=np.array(distribution)/sum(distribution)
    return distribution, distance


def cal_reachable_pt(point, r, n, p,q,distribution_array,distace):
    """calculate short range reachable points"""
    index_1 =points_within_distance(point=point,n=n,p=p)
    """calculate long range reachable points"""
    flag=0
    index_2=[]
    while len(index_2)!=q:
        long_dist=np.random.choice(distace, p=distribution_array)
        point_candidates=points_in_distance(point, n, long_dist)
        if len(point_candidates)!=0:
            index_2.append(random.choice(point_candidates))
    return np.array(index_1 + index_2)
        # else:print('again',long_dist)

def next_point(point, r, destination, n, p,q,distribution_array,distace):
    index = cal_reachable_pt(point, r, n, p,q,distribution_array,distace)
    lengths = [manhattan_pro(point_i, destination, n) for point_i in index]
    return index[np.argmin(lengths)]
