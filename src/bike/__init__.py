#coding:utf-8
from .bike import *

# FIXME: loaddata的な関数を作るべき

level = 47.6443351923
m = 55

fc4600 = Crank(0.165, [34, 50])
cs4600 = Sprocket(0.329, [12, 13, 14, 15, 17, 19, 21, 24, 27, 30])
front_wheel = rear_wheel = Wheel(1, 0.35)

farna700tiagra = Bicycle(4.8, 5.2, front_wheel, rear_wheel, fc4600, cs4600)
rider = Rider(170, m, level, farna700tiagra, 90)