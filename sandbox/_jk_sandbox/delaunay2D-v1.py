import fieldpack as fp
from fieldpack import *
import math

outie = fp.makeOut(fp.outies.Rhino, "delaunay2Dtest")


def delaunay2D(pointIn):
    numPoints = len(pointIn)
    verts = []
    verts.extend(pointIn)
    faces = []
    #triangles = fp.Mesh()
    #triangles.add_vert(verts)
    outie.put(verts)


    #Find an initial triangle enclosing all points
    xMin = verts[0].x
    yMin = verts[0].y
    xMax = xMin
    yMax = yMin
    for i in range(numPoints):
        if verts[i].x < xMin:  xMin = verts[i].x
        if verts[i].x > xMax:  xMax = verts[i].x
        if verts[i].y < yMin:  yMin = verts[i].y
        if verts[i].y > yMax:  yMax = verts[i].y
    xSpan = xMax - xMin
    ySpan = yMax - yMin
    if xSpan > ySpan:
        dSpan = xSpan
    else:
        dSpan = ySpan
    xMid = (xMin + xMax)/2.0
    yMid = (yMin + yMax)/2.0
    verts.append(Point(xMid + 2*dSpan, yMid - dSpan))
    verts.append(Point(xMid, yMid + 2*dSpan))
    verts.append(Point(xMid - 2*dSpan, yMid - dSpan))
    triangles = fp.Mesh()
    triangles.add_vert(verts)
    faces.append([numPoints, numPoints + 1, numPoints + 2])
    

    for i in range(numPoints):
    #for i in range(3):
        # for each point, search for all triangles whose circumcircle contain
        # the point;  delete these triangles (thus forming a polygon enclosing the point)
        # and form new triangles from the point to the vertices of the enclosing polygon
        p = verts[i]
        edges = []
        curFaces = []
        curFaces.extend(faces)
        for f in curFaces:
            p1 = verts[f[0]]
            p2 = verts[f[1]]
            p3 = verts[f[2]]
            #outie.put([p, p1, p2, p3, center])
            #if p is in the circumcircle, save the edges of the triangle before deleting
            #the triangle;  redundant edges are interior edges of the polygon and will
            #be removed later
	    center = calc_circumcenter(p1, p2, p3)
            if Vec(p, center).length < Vec(p1, center).length:
                edges.append([f[0],f[1]])
                edges.append([f[1],f[2]])
                edges.append([f[2],f[0]])
                faces.remove(f)
            #remove redundant edges (which leaves only the edges of the enclosing polygon)
        edges = removeDuplicates(edges)
        for j in range(len(edges)):
            faces.append([edges[j][0], edges[j][1], i])

    for f in faces:
        if f[0] > numPoints-1 or f[1] > numPoints - 1 or f[2] > numPoints - 1:
	    continue
	triangles.add_face(f[0],f[1],f[2])
 
    outie.put(triangles)
    
#determines the circumcenter of a triangle with vertices v1, v2, v3;  the circumcenter
#is the intersection of any two perpendicular bisectors of the sides of the triangle
def calc_circumcenter(v1, v2, v3):
    x1 = v1.x
    y1 = v1.y
    x2 = v2.x
    y2 = v2.y
    x3 = v3.x
    y3 = v3.y
    tol = 10e-5
    
    if math.fabs(y2-y1) < tol:
        m2 = -(x3 - x2) / (y3 - y2)
        mx2 = (x2 + x3) / 2
	my2 = (y2 + y3) / 2
	xc = (x2 + x1) / 2
	yc = m2 * (xc - mx2) + my2
    elif math.fabs(y3-y2) < tol:
	m1 = -(x2 - x1) / (y2 - y1)
	mx1 = (x1 + x2) / 2
	my1 = (y1 + y2) / 2
	xc = (x3 + x2) / 2
	yc = m1 * (xc - mx1) + my1
    else:
	m1 = -(x2 - x1) / (y2 - y1)
	m2 = -(x3 - x2) / (y3 - y2)
	mx1 = (x1 + x2) / 2
	mx2 = (x2 + x3) / 2
	my1 = (y1 + y2) / 2
	my2 = (y2 + y3) / 2
	xc = (m1 * mx1 - m2 * mx2 + my2 - my1) / (m1 - m2)
	yc = m1 * (xc - mx1) + my1

    return Point(xc, yc)
 
def removeDuplicates(a):
    "Gets a list of lists and removes the duplicates"
    #first sort the sublists
    acopy = []
    acopy.extend(a)
    acopy = [sorted(i) for i in a]
    b = []
    index = 0
    for i in acopy:
	times = 0
	for j in acopy:
	    if times > 1: continue
	    if i==j: times +=1
	if times == 1: b.append(a[index])
	index +=1
    return b

pts = []
pts.append(Point(1,0))
pts.append(Point(1,1))
pts.append(Point(2,3))
pts.append(Point(-3,4))
pts.append(Point(-2.5, 5))
pts.append(Point(5, 1))
pts.append(Point(4, -1))
pts.append(Point(2, -2))
pts.append(Point(0, -4))
pts.append(Point(1, -2))
pts.append(Point(10, 0))
delaunay2D(pts)

outie.draw()