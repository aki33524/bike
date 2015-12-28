#coding:utf-8
from crank import Crank
from wheel import Wheel
from fatigue.fatigue import get_fatigue_func_by_level, get_fatigue_func

G = 9.8
SPAN = 0.1
        
class Bicycle(object):
    def __init__(self, front_weight, rear_weight, front_wheel, rear_wheel, crank):
        self.front_weight = front_weight
        self.rear_weight = rear_weight
        self.front_wheel = front_wheel
        self.rear_wheel = rear_wheel
        self.crank = crank
        
class Rider(object):
    def __init__(self, height, weight, level, bicycle):
        self.height = height
        self.weight = weight
        self.bicycle = bicycle
        self._level = level
        self.fatigue_func = self.get_fatigue_func()
        
        
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
    
    def _get_level(self):
        return self._level
    def _set_level(self, value):
        self._level = value
        self.fatigue_func = self.get_fatigue_func()
    level = property(_get_level, _set_level)
    
    def get_fatigue_func(self):
        return get_fatigue_func_by_level(self.level)
    
    def acceleration(self, w, v, x=0):
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
    
    def get_time_by_splitted_course(self, splitted, watt=None):
        lb = 0
        ub = 10000
        for _ in range(30):
            mid = (lb + ub) / 2.
            if watt is None:
                w = self.fatigue_func(mid) * self.weight
            else:
                w = watt
            t = 0
            vel = 0
            for v in splitted:
                d = 0
                pacceleration = -1
                while d < v[0]:
                    # 実用上問題ない誤差を含む
                    acceleration = self.acceleration(w, vel, v[1] * 100. / v[0])
                    if acceleration == pacceleration:
                        t += (v[0] - d) / vel
                        d = v[0]
                    else:
                        vel += acceleration * SPAN
                        d += vel * SPAN
                        t += SPAN
                    pacceleration = acceleration
                    
            if watt is not None:
                return t
                    
            if mid < t:
                lb = mid
            else:
                ub = mid
        return mid
    
    def get_watt_by_splitted_course(self, alltime, splitted):
        lb = 0
        ub = 30 * self.weight
        for _ in range(30):
            mid = (lb + ub) / 2.
            t = self.get_time_by_splitted_course(splitted, mid)
            if t > alltime:
                lb = mid
            else:
                ub = mid
        return mid
    
    def get_level(self, t, watt):
        return get_fatigue_func(t, float(watt)/self.weight)[:2]
        