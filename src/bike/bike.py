#coding:utf-8
from crank import Crank
from wheel import Wheel

G = 9.8
SPAN = 0.1
        
class Bicycle():
    def __init__(self, front_weight, rear_weight, front_wheel, rear_wheel, crank):
        self.front_weight = front_weight
        self.rear_weight = rear_weight
        self.front_wheel = front_wheel
        self.rear_wheel = rear_wheel
        self.crank = crank
        
class Rider():
    def __init__(self, height, weight, watt, bicycle):
        self.height = height
        self.weight = weight
        self.bicycle = bicycle
        self.watt = watt
    @property
    def front_weight(self):
        return self.weight*0.4 + self.bicycle.front_weight - self.bicycle.front_wheel.weight
    @property
    def rear_weight(self):
        return self.weight*0.6 + self.bicycle.rear_weight - self.bicycle.rear_wheel.weight
    @property
    def all_weight(self):
        return self.weight + self.bicycle.front_weight + self.bicycle.rear_weight
    @property
    def K(self):
        # 空気抵抗係数 温度と表面積（身長体重から割り出せる？）に依存する
        return 0.15
    def W(self, v, x, wv=0):
        M = self.all_weight
        return v * ((0.1 * x + 0.05) * M + 0.15 * (v+wv)**2)
    def acceleration(self, w, v, x=0, boost=False):
        if v < 0:
            raise Exception("バックするな💢")
        
        M = self.all_weight
        R = self.bicycle.front_wheel.R
        
        resistor = 0
        
        # フラペの場合の限界トルク（推測）
        mf = M * G * self.bicycle.crank.length / R * 0.7
        if v == 0:
            f = mf
        else:
            f = min(w/v, mf)
            resistor += 0.005 * M * G   # 転がり抵抗
            
        if boost:
            f *= 2
            
        resistor += 0.01 * x * M * G    # 傾斜抵抗
        resistor += self.K * v**2       # 空気抵抗
        
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
    
    def get_time_by_splitted_course(self, splitted, signal, st=0):
        ok = True
        t = 0
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
            boosttime = 0
            while d < v[0]:
                vel += self.acceleration(self.watt, vel, v[1] * 100. / v[0], boosttime>0) * SPAN
                d += vel * SPAN
                t += SPAN
                boosttime -= SPAN
                
        return t-st, ok
    
    def get_watt_by_splitted_course(self, alltime, splitted, signal, st=0):
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
                boosttime = 0
                while d < v[0]:
                    vel += self.acceleration(mid, vel, v[1] * 100. / v[0], boosttime>0) * SPAN
                    d += vel * SPAN
                    t += SPAN
                    boosttime -= SPAN
                    
            if t > alltime:
                lb = mid
            else:
                ub = mid
        return mid, ok