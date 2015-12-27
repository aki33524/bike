#encoding:utf-8
from interpolation import interpolation
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

sections = interpolation(spoints)
for section in sections:
    print "%f\t%f" %section