#coding:utf-8
import xml.etree.ElementTree as ET

def get_points(filename, resolution=0):
    namespace = "{http://www.topografix.com/GPX/1/1}"

    tree = ET.parse(filename)
    root = tree.getroot()
    
    points = []
    for v in root[0][0]:
        lat, lon = float(v.attrib["lat"]), float(v.attrib["lon"])
        ele = float(v[0].text)
        point = ((ele+resolution, ele-resolution), (lat, lon))
        points.append(point)
    
    return points