#coding:utf-8
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
