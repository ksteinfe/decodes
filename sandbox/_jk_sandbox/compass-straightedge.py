import rhinoscriptsyntax as rs

#Let's work in 2D first (in Rhino, only look at Top window).
#Points in 2D can be defined by a list of numbers (x, y, 0) 
p1 = [1,12,0]
p2 = [-2,2,0]

#and drawn to the canvas by using a built-in function
rs.AddPoint(p1)
rs.AddPoint(p2)

#a line that connects two points can similarly be drawn 
line1 = rs.AddLine(p1,p2)

#as can a circle defined by a point and a radius
circ1 = rs.AddCircle(p1, 7)

#with AddLine, and Add Circle, we now have the computational equivalent of
#drawing with a compass and straightedge


def findIntersection(curve1, curve2):
	pAttempt = rs.CurveCurveIntersection(curve1,curve2)
	#if intersection exists
	if len(pAttempt) != 0:
		pOut = list()
		for i in range(len(pAttempt)):
			pInt = pAttempt[i]
			pOut.append(pInt[1])
		return pOut
	else:
		return None
	
def AddPointList(pIn):
	for i in range(len(pIn)):
		rs.AddPoint(pIn[i])
		


pInt1 = findIntersection(line1, circ1)
if pInt1 != None:
	AddPointList(pInt1)

p3 = [1.5,5,0]
rs.AddPoint(p3)
circ2 = rs.AddCircle(p3, 2)

pInt2 = findIntersection(circ1, circ2)
if pInt2 != None:
	AddPointList(pInt2)
	
#hw2.py
		
def dist(p1, p2):
	return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2+(p2[2]-p1[2])**2)
	
#p = [1,4,0]
#rs.AddPoint(p)
p1 = [10,0,0]
p2 = [-15,25,0]
line = p1,p2
rs.AddLine(line[0], line[1])


p = rs.GetPoint("Select point", rs.filter.point)
if p is None:
	print "No point selected"
#line = rs.GetObject("Select line", rs.filter.curve)
#if line is None:
#	print "No line selected"

def MakePerpLine(lineIn, pIn):
	closest = rs.LineClosestPoint(lineIn, pIn)
	rs.AddLine(closest, pIn)
				
def MakePerpLineCS(lineIn, pIn):
	#rad1 = rs.LineMinDistanceTo(lineIn, pIn) + 0.1
	rad1 = min(dist(pIn, lineIn[0]), dist(pIn, lineIn[1]))
	circ = rs.AddCircle(pIn, rad1)
	lineTest = rs.AddLine(lineIn[0], lineIn[1])
	pInt = findIntersection(lineTest, circ)
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
		

MakePerpLineCS(line, p)