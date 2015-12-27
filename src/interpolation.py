#coding:utf-8
from misc import hubeny

def interpolation(points):
    # FIXM: pointsが変わる副作用がある
    num = len(points)
    
    distances = [0]*num
    for i in range(1, num):
        distances[i] = distances[i-1] + hubeny(points[i-1][1], points[i][1])
    for i in range(num):
        points[i][1] = distances[i]
    
    start, goal = sum(points[0][0])/2, sum(points[num-1][0])/2
    L = []
    R = []
    for i in range(num):
        L.append(points[i][0][1])
        R.append(points[i][0][0])
        
    length = 0
    last_point = (start, 0)
    ly = ry = 0
    l1 = L[ly] - last_point[0]
    r1 = R[ry] - last_point[0]
    ny = 1
    
    sections = []
    sections.append((last_point[0], points[last_point[1]][1]))
    while ny < num:
        l2 = float(L[ny] - last_point[0]) / (points[ny][1] - points[last_point[1]][1])
        r2 = float(R[ny] - last_point[0]) / (points[ny][1] - points[last_point[1]][1])
        if r1 <= l2:
            length += ((R[ry] - last_point[0]) ** 2 + (points[ry][1] - points[last_point[1]][1]) ** 2) ** 0.5
            sections.append((R[ry], points[ry][1]))
            last_point = (R[ry], ry)
            ry = ly = ry + 1
            l1 = L[ry] - last_point[0]
            r1 = R[ry] - last_point[0]
            ny = ry
        elif r2 <= l1:
            length += ((L[ly] - last_point[0]) ** 2 + (points[ly][1] - points[last_point[1]][1]) ** 2) ** 0.5
            sections.append((L[ly], points[ly][1]))
            last_point = (L[ly], ly)
            ly = ry = ly + 1
            l1 = L[ly] - last_point[0]
            r1 = R[ry] - last_point[0]
            ny = ly
        else:
            if l1 <= l2:
                ly = ny
                l1 = l2
            if r2 <= r1:
                ry = ny
                r1 = r2
        ny += 1
    g = float(goal - last_point[0]) / (points[num-1][1] - points[last_point[1]][1])
    if r1 <= g:
        length += ((R[ry] - last_point[0]) ** 2 + (points[ry][1] - points[last_point[1]][1]) ** 2) ** 0.5
        sections.append((R[ry], points[ry][1]))
        last_point = (R[ry], ry)
    elif g <= l1:
        length += ((L[ly] - last_point[0]) ** 2 + (points[ly][1] - points[last_point[1]][1]) ** 2) ** 0.5
        sections.append((L[ly], points[ly][1]))
        last_point = (L[ly], ly)
    length += ((goal - last_point[0]) ** 2 + (points[num-1][1] - points[last_point[1]][1]) ** 2) ** 0.5
    sections.append((goal, points[num-1][1]))
    return sections
    
    
    
    