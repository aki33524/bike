#coding:utf-8
import numpy as np
from scipy.optimize import curve_fit
from __init__ import WEIGHT_POWER_RATIO, LEVEL

def get_fatigue_func_by_idx(idx):
    def model_func1(x, a, b):
        return a * np.power(x, b)
    
    def model_func2(x, a, b):
        return a * np.log(x) + b
    
    xx = [5, 60, 300, 10000]
    yy = WEIGHT_POWER_RATIO[idx]
    x = np.array(xx[:3])
    y = np.array(yy[:3])
    
    popt1, pcov = curve_fit(model_func1, x, y)
    y1 = model_func1(x, *popt1)
    
    popt2, pcov = curve_fit(model_func2, x, y)
    y2 =  model_func2(x, *popt2)
    
    a, b = 0, 1
    for i in range(100):
        c1, c2 = (a + b) / 3., (a + b) * 2 / 3.
        error1 = sum((c1*y1 + (1-c1)*y2 - y) ** 2)
        error2 = sum((c2*y1 + (1-c2)*y2 - y) ** 2)
        if error1 > error2:
            a = c2
        else:
            b = c1
            
    def func(x):
        if x < 0:
            raise "正の時間運動しろ💢"
        elif x < xx[2]:
            return a*model_func1(x, *popt1) + (1-a)*model_func2(x, *popt2)
        elif x < xx[3]:
            return (x - xx[2]) * (yy[3] - yy[2]) /(xx[3] - xx[2]) + yy[2]
        else:
            return yy[3]
    return func

def get_fatigue_func_by_level(level):
    a = level - int(level)
    b = int(level+1) - level
        
    def func(t):
        f1 = get_fatigue_func_by_idx(int(level))
        f2 = get_fatigue_func_by_idx(int(level+1))
        return b*f1(t) + a*f2(t)
    
    return func

def get_fatigue_func(t, watt):
    lb = 0
    ub = len(WEIGHT_POWER_RATIO)
    
    while lb + 1 < ub:
        mid = (lb + ub)/2
        if watt < get_fatigue_func_by_idx(mid)(t):
            lb = mid
        else:
            ub = mid
            
    if lb == 0:
        raise "豪脚おじさん💢"
    if ub == len(WEIGHT_POWER_RATIO):
        raise "トレーニングして💢"
    
    f1 = get_fatigue_func_by_idx(lb)
    f2 = get_fatigue_func_by_idx(ub)
    for i in range(100):
        mid = (lb + ub)/2.
        a = mid - lb
        b = ub - mid
        if watt < b*f1(t) + a*f2(t):
            lb = mid
        else:
            ub = mid
    
    def func(t):
        return b*f1(t) + a*f2(t)        
    
    for i, v in enumerate(LEVEL):
        if mid < v[0]:
            if i == 0:
                return (0, mid, LEVEL[i][0]), "〜 " + v[1], func
            else:
                return (LEVEL[i-1][0], mid, LEVEL[i][0]), LEVEL[i-1][1] + " 〜 " + LEVEL[i][1], func
    return (LEVEL[-1][0], mid, len(WEIGHT_POWER_RATIO)-1), LEVEL[-1][1] + " 〜", func
            
    