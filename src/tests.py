#coding:utf-8
import os
import unittest
import google
import rootlab
from interpolation import interpolation
from misc import points_to_sections
from bike import Crank, Sprocket, Wheel, Bicycle, Rider

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_filepath(filepath):
    return os.path.join(BASE_DIR, filepath)

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.time = 1752
        self.watt = 142.949209968
        self.level = 47.64042943316461
        
        fc4600 = Crank(0.165, [34, 50])
        cs4600 = Sprocket(0.329, [12, 13, 14, 15, 17, 19, 21, 24, 27, 30])
        front_wheel = rear_wheel = Wheel(1, 0.35)
        farna700tiagra = Bicycle(4.8, 5.2, front_wheel, rear_wheel, fc4600, cs4600)
        self.rider = Rider(farna700tiagra, 170, 55)
    
    def test_get_watt_by_splitted_course(self):
        """コースとタイムからレベルを算出する デフォルトではレベル設定も行う"""
        points = google.get_points(get_filepath("googledata/katsuoji.txt"))
        sections = points_to_sections(interpolation(points))
        watt, gear_change, verbose_data, message = self.rider.get_watt_by_splitted_course(self.time, sections)
#         print watt
#         print message
    
    def test_capability(self):
        """レベルから実力を算出する"""
        self.rider.level = self.level
        levels, text = self.rider.capability
#         print levels, text
        
    def test_get_time_by_splitted_course(self):
        """コースとレベルからタイムを算出する"""
        # Thanks to http://latlonglab.yahoo.co.jp/route/watch?id=f9b389b9434df4292d74a5a94c9a7ea9
        self.rider.level = self.level
        points = rootlab.get_points(get_filepath("gpxdata/富士ヒルクライム.gpx"), 15)
        sections = points_to_sections(interpolation(points))
        time, gear_change, verbose_data, message = self.rider.get_time_by_splitted_course(sections)
#         print "time:", time
#         print message
#         print "タイム\tケイデンス\tフロントギア\tリアギア\t距離\t勾配"
#         for i in range(0, len(verbose_data), 10):
#             data = verbose_data[i]
#             print "%f\t%f\t%d\t%d\t%f\t%f" %\
#                 (data["time"], data["cadence"], data["gear"][0], data["gear"][1], data["distance"], data["grad"])
                
        
if __name__ == '__main__':
    unittest.main()