#coding:utf-8
from misc import hubeny

def calcDeg(ax, ay, bx, by, cx, cy):
    # 反時計回り
    return (by-ay)*(cx-ax)-(bx-ax)*(cy-ay) > 0

def interpolation(points):
    N = len(points)
    
    dist = [0]*N
    for i in range(1, N):
        dist[i] = dist[i-1] + hubeny(points[i-1][1], points[i][1])
    
    start, goal = sum(points[0][0])/2, sum(points[-1][0])/2
    L = [p[0][1] for p in points]
    R = [p[0][0] for p in points]
    L.append(goal)
    R.append(goal)
    
    total = 0
    ax = 0
    ay = start
    sections = []
    sections.append((ay, total))
    x = ax + 1
    lx = x
    rx = x
    
    while x < N:
        bx = 0
        by = 0
        if not calcDeg(dist[ax], ay, dist[lx], L[lx], dist[x], L[x]):
            lx = x
            if rx < x and not calcDeg(dist[ax], ay, dist[rx], R[rx], dist[x], L[x]):
                bx = rx
                by = R[rx]
        if calcDeg(dist[ax], ay, dist[rx], R[rx], dist[x], R[x]):
            rx = x
            if lx < x and calcDeg(dist[ax], ay, dist[lx], L[lx], dist[x], R[x]):
                bx = lx
                by = L[lx]
        if bx != 0:
            total += ((dist[bx]-dist[ax])**2 + (by-ay)**2) ** 0.5
            sections.append((by, total))
            ax = bx
            ay = by
            lx = rx = x = ax + 1
        x += 1
        
    total += ((dist[ax]-dist[-1])**2 + (ay-goal)**2) ** 0.5
    sections.append((goal, total))
    return sections
