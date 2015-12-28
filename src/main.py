#coding:utf-8
import google
import rootlab
from interpolation import interpolation
from bike import rider
from misc import points_to_sections

from fatigue.fatigue import get_fatigue_func_by_level

points = google.get_points("googledata/katsuoji.txt")
sections = points_to_sections(interpolation(points))
t = 1752
watt, message = rider.get_watt_by_splitted_course(t, sections)
level, txt =  rider.get_level(t, watt)
print message
print txt
print level[0], level[1], level[2]
rider.level = level[1]

# Thanks to http://latlonglab.yahoo.co.jp/route/watch?id=f9b389b9434df4292d74a5a94c9a7ea9
points = rootlab.get_points("gpxdata/富士ヒルクライム.gpx", 15)
sections = points_to_sections(interpolation(points))
time, gear_change, message = rider.get_time_by_splitted_course(sections)

print "time:", time
for v in gear_change:
    print v[0], v[1]
print message

