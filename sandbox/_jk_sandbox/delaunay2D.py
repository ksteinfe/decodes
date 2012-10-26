import fieldpack as fp
from fieldpack import *
import math
TOL = 1e-9

outie = fp.makeOut(fp.outies.Rhino, "delaunay2Dtest")

    
class Triangle():
    def __init__(self, v, f):
	self._vert = v
	self._face = f # ordered in a counterclockwise manner

    def vert(self): return self._vert	
    def face(self): return self._face
	  
    def circumcenter(self):
	x1 = self._vert[0].x
	y1 = self._vert[0].y
	x2 = self._vert[1].x
	y2 = self._vert[1].y
	x3 = self._vert[2].x
	y3 = self._vert[2].y
    
	if math.fabs(y2-y1) < TOL:
	    m2 = -(x3 - x2) / (y3 - y2)
	    mx2 = (x2 + x3) / 2
	    my2 = (y2 + y3) / 2
	    xc = (x2 + x1) / 2
	    yc = m2 * (xc - mx2) + my2
	elif math.fabs(y3-y2) < TOL:
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
    
    def in_circumcircle(self, pt):
	pv = self._vert[0]
	pc = self.circumcenter()
	if (((pc.x - pt.x)**2 + (pc.y - pt.y)**2) < ((pc.x - pv.x)**2 + (pc.y - pv.y)**2)):
	    return True
	else: return False


def delaunay2D(verts):
    numPoints = len(verts)
    triangles = []

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
    triangles.append(Triangle([verts[numPoints], verts[numPoints+1], verts[numPoints + 2]],
	[numPoints, numPoints + 1, numPoints + 2]))
     
    for i in range(numPoints):
        # for each point, search for all triangles whose circumcircle contain
        # the point;  delete these triangles (thus forming a polygon enclosing the point)
        # and form new triangles from the point to the vertices of the enclosing polygon
        p = verts[i]
        edges = []
	curTriangles = []
        curTriangles.extend(triangles)
        for t in curTriangles:
            if t.in_circumcircle(p):
		edges.append([t._face[0],t._face[1]])
                edges.append([t._face[1],t._face[2]])
                edges.append([t._face[2],t._face[0]])
                triangles.remove(t)
	#remove redundant edges (which leaves only the edges of the enclosing polygon)
	edges = removeDuplicates(edges)
 	for e in edges:
	    triangles.append(Triangle([verts[e[0]], verts[e[1]], verts[i]] ,[e[0], e[1], i]))
    
    #TODO: implement a draw functionality for Triangle
    trianglesDraw = fp.Mesh()
    trianglesDraw.add_vert(verts)
    for t in triangles:
        if t._face[0] > numPoints-1 or t._face[1] > numPoints - 1 or t._face[2] > numPoints - 1:
	    continue
	trianglesDraw.add_face(t._face[0],t._face[1],t._face[2])
    
    outie.put(verts)
    outie.put(trianglesDraw)
    
    
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



if __name__=="__main__":
    pts = []
    ptFile = open("./ptCloud2D.txt", 'r')
    for line in ptFile:
	fld = line.split()
	x = float(fld[0])
	y = float(fld[1])
	pts.append(Point(x,y))
 
    delaunay2D(pts)   
    

    outie.draw()