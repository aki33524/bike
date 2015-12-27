#coding:utf-8
import google
import rootlab

print google.get_points("googledata/katsuoji.txt")

# Thanks to http://latlonglab.yahoo.co.jp/route/watch?id=f9b389b9434df4292d74a5a94c9a7ea9
print rootlab.get_points("gpxdata/富士ヒルクライム.gpx", 10)