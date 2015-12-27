#encoding:utf-8
import googlemaps

# TODO:座標から自動コンバート

def get_points(filename, resolution=9):
    # FIXME: 本来elevation apiを用いた時はresolutionが取れるのでこれは不要
    f = open(filename)
    resolution = 9
    
    points = []
    for line in f.readlines():
        height, lat, lng = map(float, line.split()) 
        points.append([(height+resolution, height-resolution), (lat, lng)])
    
    return points