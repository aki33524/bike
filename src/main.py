#coding:utf-8



# w = 300
# m = 55
# wheel = 1
# bicycle1 = Bicycle(4.8, 5.2, Wheel(wheel, 0.7), Wheel(wheel, 0.7), Crank(0.165))
# rider1 = Rider(170, m-1, w, bicycle1)
# 
# wheel = 0.5
# bicycle2 = Bicycle(4.8-1+wheel, 5.2-1+wheel, Wheel(wheel, 0.7), Wheel(wheel, 0.7), Crank(0.165))
# rider2 = Rider(170, m, w, bicycle2)
# 
# v1, v2 = 0, 0
# x1, x2 = 0, 0
# grad = 10
# for i in range(int(100/SPAN)):
#     v1 += rider1.acceleration(v1, grad) * SPAN
#     x1 += v1 * SPAN
#     v2 += rider2.acceleration(v2, grad) * SPAN
#     x2 += v2 * SPAN
#     if i % int(1/SPAN) == 0:
#         print x2 - x1


s = [(100, (0, 60)), (100, (15, 60)), (100, (0, 0)), (100, (55, 0)), (100, (90, 35)), (100, (0, 0)), (100, (0, 0))]
l = [(500, -10), (800, 10), (1000, 0), (900, -14), (850, -2), (850, 18), (200, -2)]

s = s[4:] + s[:4]
l = l[4:] + l[:4]
s[0] = (100, (0, 0))

w = 300
m = 55
wheel = 1
from bike import *
bicycle = Bicycle(4.8, 5.2, Wheel(wheel, 0.7), Wheel(wheel, 0.7), Crank(0.165))
rider = Rider(170, m, w, bicycle)
print rider.get_watt_by_splitted_course(600, l, s)

# for t in range(560, 600):
#     print t
#     ll = []
#     for i in range(100):
#         w, ok = get_time_by_splitted_course(t, l, s, i)
#         if ok:
#             ll.append(i)
#     print w, ll