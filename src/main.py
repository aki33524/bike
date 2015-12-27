#coding:utf-8
import google
import rootlab
from interpolation import interpolation
from bike import rider
from misc import points_to_sections

points = google.get_points("googledata/katsuoji.txt")
sections, signals = points_to_sections(interpolation(points))
print rider.get_watt_by_splitted_course(1752, sections, signals)

# Thanks to http://latlonglab.yahoo.co.jp/route/watch?id=f9b389b9434df4292d74a5a94c9a7ea9
points = rootlab.get_points("gpxdata/富士ヒルクライム.gpx", 15)
sections, signals = points_to_sections(interpolation(points))
print rider.get_time_by_splitted_course(sections, signals)