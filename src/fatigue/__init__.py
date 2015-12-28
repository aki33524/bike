#coding:utf-8
import os


# Thanks to http://www.bicycling.com/training/fitness/trainingpeaks-power-profiles-cyclists
WEIGHT_POWER_RATIO = []
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "weight_power_ratio.txt")) as f:
    for line in f.readlines():
        WEIGHT_POWER_RATIO.append(map(float, line.split("\t")))

LEVEL = []
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "level.txt")) as f:
    for line in f.readlines():
        level, string = line.split("\t")
        LEVEL.append((int(level), string.replace("\n", "")))