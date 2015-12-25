#encoding:utf-8
import math as m

G = 9.8
R = 0.7
SPAN = 0.1

def W(v, x, M=55 + 10, wv=0):
    return v * ((0.1 * x + 0.05) * M + 0.15 * (v+wv)**2)

def acceleration(w, v, x=0, M=65, k=0.15):
    if v < 0:
        raise Exception("バックするな💢")
    
    resistor = 0
    resistor += 0.01 * x * M * G    # 傾斜抵抗
    resistor += k * v**2            # 空気抵抗
    resistor += 0.005 * M * G       # 転がり抵抗
    
    mf = M*G*0.165/0.7*0.7          # 筋力限界
    if v == 0:
        f = mf
    else:
        f = min(w/v, mf)
        
    I = (R**2 + (R-0.05)**2) * 1.0 / 2 * 2 #慣性モーメント
    return (f - resistor) * R**2 / (R**2 * M + I)

def get_speed_by_grad(w, x):
    lb = 0
    ub = 100
    for i in range(100):
        mid = (lb + ub) / 2.
        if W(mid, x) < w:
            lb = mid
        else:
            ub = mid
    return mid

def get_time_by_splitted_course(alltime, splitted, signal, st=0):
    alltime += st
    lb = 0
    ub = 10000
    for _ in range(100):
        ok = True
        mid = (lb + ub) / 2.
        t = st
        vel = 0
        for i, v in enumerate(splitted):
            s = signal[i]
            per = s[0]
            bs, be = s[1]
#                 bs += 5
#                 be -= 5
            if bs >= be:
                be += per
            ok &= (bs <= t % per <= be or bs <= t % per + 100 <= be)
            
            d = 0
            while d < v[0]:
                vel += acceleration(mid, vel, v[1] * 100. / v[0]) * SPAN
                d += vel * SPAN
                t += SPAN
            
        if t > alltime:
            lb = mid
        else:
            ub = mid
    return mid, ok

s = [(100, (0, 60)), (100, (15, 60)), (100, (0, 0)), (100, (55, 0)), (100, (90, 35)), (100, (0, 0)), (100, (0, 0))]
l = [(500, -10), (800, 10), (1000, 0), (900, -14), (850, -2), (850, 18), (200, -2)]

s = s[4:] + s[:4]
l = l[4:] + l[:4]
s[0] = (100, (0, 0))


print get_time_by_splitted_course(500, l, s)
for t in range(500, 600):
    print t
    ll = []
    for i in range(100):
        w, ok = get_time_by_splitted_course(t, l, s, i)
        if ok:
            ll.append(i)
    print w, ll