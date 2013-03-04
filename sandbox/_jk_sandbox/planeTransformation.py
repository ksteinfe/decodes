
#Plane Transformations

#Note, this only will do what you expect when these transformations are acting on points in 2D

import rhinoscriptsyntax as rs

# Move takes as input a start point and an end point which represents the displacement vector
	
def Move(startPoint, endPoint, pIn):
	return rs.VectorAdd(pIn,rs.VectorSubtract(endPoint,startPoint))


def MoveX(startPoint, endPoint, pIn):
	matrix = rs.XformTranslation(rs.VectorSubtract(endPoint, startPoint))
	return rs.PointTransform(pIn, matrix)


origin = [0,0,0]
start = [-4,2,0]
end = [-1,1,0]
p = [4, 5, 0]

print Move(start, end, p)	
print MoveX(start, end, p)


# Mirror takes a reflection axis which in 2D could be represented by a line.  Here I will
# show some of the technicalities between representing an axis (an infinite line) by
# a line segment

# Let's start off with a slightly altered version of what we used for MakePerpLine.  Note
# that this only works if the perpendicular line through p intersects the line segment p1, p2
# since LineClosestPoint literally returns the closest point on the line segment to pIn.
def MirrorTake1(lineIn, pIn):
	closest = rs.LineClosestPoint(lineIn, pIn)
	return rs.VectorAdd(closest, rs.VectorSubtract(closest, pIn))

p1 = [10,0,0]
p2 = [-15,25,0]
line = p1,p2
rs.AddLine(line[0], line[1])

print MirrorTake1(line, p)
rs.AddPoint(p)
rs.AddPoint(MirrorTake1(line, p))
#if we give it a point whose perp line does not intersect with the line segment, we get
#something different than what we want
pOff = [7,-10,0]
rs.AddPoint(pOff)
rs.AddPoint(MirrorTake1(line, pOff))

#With the help of vectors, we can write a function called LineProjectedPoint which returns the
#closest projected point treating the line as an infinite line
def LineProjectedPoint(lineIn, pIn):
	pLine0 = lineIn[0]
	pLine1 = lineIn[1]
	u = rs.VectorUnitize(rs.VectorSubtract(pLine1, pLine0))
	projectedScale = rs.VectorDotProduct(rs.VectorSubtract(pIn, pLine0), u)
	return rs.VectorAdd(pLine0, rs.VectorScale(u, projectedScale))
	
rs.AddPoint(LineProjectedPoint(line, pOff))

#now we can write a Mirror function that does what we want
def Mirror(lineIn, pIn):
	projected = LineProjectedPoint(lineIn, pIn)
	if dist(projected, pIn) > rs.UnitAbsoluteTolerance(10**(-5), True):
		return rs.VectorAdd(projected, rs.VectorSubtract(projected, pIn))
	else:
		return pIn
	

print Mirror(line, pOff)
rs.AddPoint(Mirror(line, pOff))

def MirrorX(lineIn, pIn):
	pLine0 = lineIn[0]
	pLine1 = lineIn[1]
	normal = rs.VectorUnitize(rs.VectorCrossProduct([0,0,1], rs.VectorSubtract(pLine1, pLine0)))
	matrix = rs.XformMirror(pLine1, normal)
	return rs.PointTransform(pIn, matrix)

print MirrorX(line, pOff)

# Rotate takes a center point, angle of rotation (measured in a counterclockwise manner)
# Much easier to do with matrix transformation
def RotateX(centerPoint, angle, pIn):
	matrix = rs.XformRotation2(angle, [0,0,1], centerPoint)
	return rs.PointTransform(pIn, matrix)

center = [-7, -6, 0]	
N = 20
for i in range(N):
	rs.AddPoint(RotateX(center, i*360/float(N), rs.VectorAdd(center, [3,0,0])))


#Scale takes a center of scale and a scale factor
def ScaleX(startPoint, factor, pIn):
	matrix = rs.XformScale(factor, startPoint)
	return rs.PointTransform(pIn, matrix)

#easier to see what scaling does when acting on a line segment
p1Scale = ScaleX(center, 0.3, p1)
p2Scale = ScaleX(center, 0.3, p2)
rs.AddLine(p1Scale, p2Scale)

def AddVector(vecdir, base_point):
	if base_point==None:
		base_point = [0,0,0]
	tip_point = rs.PointAdd(base_point, vecdir)
	line = rs.AddLine(base_point, tip_point)
	if line:
		return rs.CurveArrows(line, 2)




v1 = [1,5,0]
v2 = [2,4,0]

#print rs.Distance(v1,v2)
#print rs.VectorAdd(v1,v2)
#print rs.VectorScale(v1, 5)
#print rs.VectorSubtract(v1,v2)



#AddVector(v1, origin)
#AddVector(v2, origin)
#AddVector(rs.VectorSubtract(v1,v2), v2)


#Warning;  this is only useful in 2D - please check your points have z = 0

#We assume the line is given, and that the point is specified by the user
#p1 = [10,0,0]
#p2 = [-15,25,0]
#line = p1,p2 #interpreted as an infinite line
#rs.AddLine(line[0], line[1])
 
#p = rs.GetPoint("Select point", rs.filter.point)
 
#Input:  a line (right now, it requires a line specified as above) and a point p
#Output:  a perpendicular line drawn on the Rhino canvas
def MakePerpLineCS(lineIn, pIn):
	rad1 = min(dist(pIn, lineIn[0]), dist(pIn, lineIn[1]))
	circ = rs.AddCircle(pIn, rad1)
	lineSegment = rs.AddLine(lineIn[0], lineIn[1])
	pInt = findIntersection(lineSegment, circ)
	if pInt != None:
		#AddPointList(pInt)
		rad2 = dist(pIn, pInt[0])+0.1
		circ1 = rs.AddCircle(pInt[0], rad2)
		circ2 = rs.AddCircle(pInt[1], rad2)    
		pInt2 = findIntersection(circ1, circ2)
		if pInt2 != None:
			#AddPointList(pInt2)
			rs.AddLine(pInt2[0],pInt2[1])
		rs.DeleteObjects([circ,circ1,circ2])


#MakePerpLineCS(line, p)




