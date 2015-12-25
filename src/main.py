#encoding:utf-8

G = 9.8
SPAN = 5

class Wheel():
    def __init__(self, weight, R):
        self.weight = weight
        self.R = R

    @property
    def I(self):
        # 簡単のため質点が外周にあるとする
        # チューブ+タイヤを300gとする
        tire = 0.3
        return self.R**2 * (self.weight + tire)

class Crank():
    def __init__(self, length):
        self.length = length
        
class Bicycle():
    def __init__(self, front_weight, rear_wheght, front_wheel, rear_wheel, crank):
        self.front_weight = front_weight
        self.rear_wheght = rear_wheght
        self.front_wheel = front_wheel
        self.rear_wheel = rear_wheel
        self.crank = crank
        
class Rider():
    def __init__(self, height, weight, bicycle):
        self.height = height
        self.weight = weight
        self.bicycle = bicycle
        
    @property
    def front_weight(self):
        return self.weight*0.4 + self.bicycle.front_weight - self.bicycle.front_wheel.weight
    
    @property
    def rear_weight(self):
        return self.weight*0.6 + self.bicycle.rear_weight - self.bicycle.rear_wheel.weight
    
    @property
    def weight(self):
        return self.weight + self.bicycle.front_weight + self.bicycle.rear_weight

    @property
    def K(self):
        # 空気抵抗係数 温度と表面積（身長体重から割り出せる？）に依存する
        return 0.15
    
    def W(self, v, x, wv=0):
        M = self.weight
        return v * ((0.1 * x + 0.05) * M + 0.15 * (v+wv)**2)

    def acceleration(self, w, v, x=0):
        if v < 0:
            raise Exception("バックするな💢")
        
        M = self.weight
        R = self.bicycle.front_wheel.R
        
        resistor = 0
        resistor += 0.01 * x * M * G    # 傾斜抵抗
        resistor += self.K * v**2       # 空気抵抗
        resistor += 0.005 * M * G       # 転がり抵抗
        
        # フラペの場合の限界トルク（推測）
        mf = M * G * self.bicycle.crank.length / R * 0.7
        
        if v == 0:
            f = mf
        else:
            f = min(w/v, mf)
        
        I = self.bicycle.front_wheel.I + self.bicycle.rear_wheel.I #慣性モーメント
        return (f - resistor) * R**2 / (R**2 * M + I)

    def get_speed_by_grad(self, w, x):
        lb = 0
        ub = 100
        for i in range(100):
            mid = (lb + ub) / 2.
            if self.W(mid, x) < w:
                lb = mid
            else:
                ub = mid
        return mid

    def get_time_by_splitted_course(self, alltime, splitted, signal, st=0):
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
                    vel += self.acceleration(mid, vel, v[1] * 100. / v[0]) * SPAN
                    d += vel * SPAN
                    t += SPAN
                
            if t > alltime:
                lb = mid
            else:
                ub = mid
        return mid, ok


bicycle = Bicycle(4.8, 5.2, Wheel(1, 0.7), Wheel(1, 0.7), Crank(0.165))
rider = Rider(170, 55, bicycle)


s = [(100, (0, 60)), (100, (15, 60)), (100, (0, 0)), (100, (55, 0)), (100, (90, 35)), (100, (0, 0)), (100, (0, 0))]
l = [(500, -10), (800, 10), (1000, 0), (900, -14), (850, -2), (850, 18), (200, -2)]

s = s[4:] + s[:4]
l = l[4:] + l[:4]
s[0] = (100, (0, 0))


print rider.get_time_by_splitted_course(300, l, s)

# for t in range(560, 600):
#     print t
#     ll = []
#     for i in range(100):
#         w, ok = get_time_by_splitted_course(t, l, s, i)
#         if ok:
#             ll.append(i)
#     print w, ll