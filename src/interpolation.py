#coding:utf-8

def func(points):
    num = len(points)
    
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
    sections.append((last_point[0], points[last_point[1]][1]))
    
    
#     print length
#     for v in sections:
#         print "%f\t%f" % (v[0], v[1])
    return sections
#     print len(sections)

f = open("katsuoji.txt")
resolution = 9

spoints = []
while True:
    points = []
    try:
        num, distance = map(int, f.readline().split())
    except ValueError:
        break
    for i in range(num):
        height, lat, lng = map(float, f.readline().split())
        points.append([(height+resolution, height-resolution), (lat, lng)])    

    distances = []
    for i in range(len(points)):
        if i == 0:
            distances.append(0)
        else:
            u, v = points[i-1][1], points[i][1]
            distances.append(((u[0]-v[0])**2 + (u[1]-v[1])**2)**0.5)
    
    for i, point in enumerate(points):
        point[1] = distance * distances[i] / sum(distances)
    
    spoints += points
    
for i in range(1, len(spoints)):
    spoints[i][1] += spoints[i-1][1]
    
# for point in spoints:
#     print point

sections = func(spoints)
for section in sections:
    print "%f\t%f" %section

# sections = []
# for i in range(5):
#     sections += func(f, resolution)
    
    
# d = sum(section[1] for section in sections)
# print d
# for section in sections:
#     section[1] = distance * section[1] / d
# 
# for section in sections:
#     print section
    