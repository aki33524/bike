#coding:utf-8
import math

# Thanks to http://blogs.yahoo.co.jp/qga03052/33991636.html
def deg2rad(deg):
    return( deg * (2 * math.pi) / 360 )

def hubeny(p1, p2) :
    lat1, lon1 = p1
    lat2, lon2 = p2
    
    a =6378137.000
    b =6356752.314140
    e =math.sqrt( (a**2 - b**2) / a**2 )
    e2 =e**2
    mnum =a * (1 - e2)
    
    my =deg2rad((lat1+lat2) /2.0)
    dy =deg2rad( lat1-lat2)
    dx =deg2rad( lon1-lon2)
    sin =math.sin(my)
    w =math.sqrt(1.0-e2 * sin *sin)
    m =mnum /(w *w *w)
    n =a/w
    dym =dy*m
    dxncos=dx*n*math.cos(my)
    
    return( math.sqrt( dym**2 + dxncos**2) )

def points_to_sections(points):
    # FIXME: 便宜上作るがゆくゆくは消したい
    sections = []
    for i in range(len(points)-1):
        p, q = points[i], points[i+1]
        sections.append((q[1]-p[1], q[0]-p[0]))
    
    return sections
    
    
    