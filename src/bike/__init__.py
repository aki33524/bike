#coding:utf-8
from .bike import *

# FIXME: loaddata的な関数を作るべき

w = 142.92936224462528
m = 55
wheel = 1
bicycle = Bicycle(4.8, 5.2, Wheel(wheel, 0.7), Wheel(wheel, 0.7), Crank(0.165))
rider = Rider(170, m, w, bicycle)