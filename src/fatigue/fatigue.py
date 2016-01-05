#coding:utf-8
from __init__ import WEIGHT_POWER_RATIO, LEVEL
from math import factorial as fac

def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

def bezier(points, t):
    N = len(points)
    sx = 0
    sy = 0
    for i in range(N):
        sx += points[i][0] * binomial(N-1,i) * t**i * (1-t)**(N-1-i)
        sy += points[i][1] * binomial(N-1,i) * t**i * (1-t)**(N-1-i)
        
    return (sx, sy)
    
def get_fatigue_func_by_level_idx(idx):
    x = [5, 60, 300, 3600]
    y = WEIGHT_POWER_RATIO[idx]
    N = len(x)
    l = []
    for i in range(N-2):
        c1 = (y[i+2] - y[i]) / (x[i+2] - x[i])
        c2 = y[i+1] - x[i+1]*c1
        l.append((c1, c2))
    points = []
    points.append((x[0], l[0][0]*x[0]+l[0][1]))
    for i in range(len(l)-1):
        xt = -(l[i][1] - l[i+1][1]) / (l[i][0]-l[i+1][0])
        yt = l[i][0]*xt + l[i][1]
        points.append((xt, yt))
    points.append(((y[-1]-l[-1][1])/l[-1][0], y[-1]))
    
    def func(t):
        if t < x[0]:
            return y[0]
        elif x[-1] < t:
            return y[-1]
        else:
            for i in range(N):
                if t < x[i]:
                    break
            lb, ub = 0, 1
            for _ in range(30):
                mid = (lb + ub) / 2.
                p = bezier(((x[i-1], y[i-1]), points[i-1], (x[i], y[i])), mid)
                if p[0] < t:
                    lb = mid
                else:
                    ub = mid
            return p[1]
                    
    return func

def get_fatigue_func_by_level(level):
    a = level - int(level)
    b = int(level+1) - level
        
    def func(t):
        f1 = get_fatigue_func_by_level_idx(int(level))
        f2 = get_fatigue_func_by_level_idx(int(level+1))
        return b*f1(t) + a*f2(t)
    
    return func

def get_level(t, ratio):
    lb = 0
    ub = len(WEIGHT_POWER_RATIO)
    
    while lb + 1 < ub:
        mid = (lb + ub)/2
        if ratio < get_fatigue_func_by_level_idx(mid)(t):
            lb = mid
        else:
            ub = mid
            
    if lb == 0:
        raise "豪脚おじさん💢"
    if ub == len(WEIGHT_POWER_RATIO):
        raise "トレーニングして💢"
    
    f1 = get_fatigue_func_by_level_idx(lb)
    f2 = get_fatigue_func_by_level_idx(ub)
    for i in range(100):
        mid = (lb + ub)/2.
        a = mid - int(mid)
        b = int(mid+1) - mid
        if ratio < b*f1(t) + a*f2(t):
            lb = mid
        else:
            ub = mid
    
    return mid    

def get_capability(level):
    for i, v in enumerate(LEVEL):
        if level < v[0]:
            if i == 0:
                return (0, level, LEVEL[i][0]), "〜 " + v[1]
            else:
                return (LEVEL[i-1][0], level, LEVEL[i][0]), LEVEL[i-1][1] + " 〜 " + LEVEL[i][1]
    return (LEVEL[-1][0], level, len(WEIGHT_POWER_RATIO)-1), LEVEL[-1][1] + " 〜"