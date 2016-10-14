from decodes import *
from decodes.core import *
from decodes.core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("processing_out loaded")

class ProcessingOut(outie.Outie):
    """outie for pushing stuff to a processing applet"""
    
    def __init__(self,applet,camera):
        super(ProcessingOut,self).__init__()
        self.app = applet
        self.cam = camera
        
        # here we can initialize stuff based on the app we've been passed
        # but we cannot draw to the app, lest raise an error 
        
    def _startDraw(self):
        #print 'i have started to draw stuff to the outie'
        
        self.app.noStroke()
        self.app.fill(0)
        self.app.pushMatrix()
        self.app.translate(0,0,0);
        self.app.sphereDetail(16)
        sphere(4);
        self.app.popMatrix()
        
        wcs_size = 20
        self.app.stroke(0)
        strokeWeight(4)
        self.app.line(0,0,0,wcs_size,0,0)
        strokeWeight(3)
        self.app.line(0,0,0,0,wcs_size*0.5,0)
        strokeWeight(2)
        self.app.line(0,0,wcs_size*0.25,0,0,wcs_size*0.5)
        
        self.app.stroke(0)
        strokeWeight(1)
        self.app.noFill()
        self.app.sphereDetail(0)
        
        if hasattr(self, 'color'):
            print('this outie has been assigned a color, i should set the pen now')
    
    def _endDraw(self):
        #print 'i have finihsed drawing stuff to the outie'
        pass
        
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        if hasattr(g, 'props') and 'color' in g.props:
            print('this object has its own color assigned')
        
        if isinstance(g, Mesh) : 
            return self._drawMesh(g)
        if isinstance(g, CS) : 
            return self._drawCS(g)
        if isinstance(g, CylCS) :
            return self._drawCylCS(g)
        if isinstance(g, LinearEntity) : 
            return self._drawLinearEntity(g)
        if isinstance(g, Point) : 
            return self._drawPoint(g)
        if isinstance(g, Vec) : 
            return self._drawVec(g)
        if isinstance(g, PLine) : 
            return self._drawPline(g)
        if isinstance(g, PGon) : 
            return self._drawPGon(g)
		
        return False

    def _drawVec(self, vec):
        return True

    def _drawPoint(self, pt):
        x = self.app.screenX(pt.x,pt.y,pt.z)
        y = self.app.screenY(pt.x,pt.y,pt.z)
        #z = self.app.screenZ(pt.x,pt.y,pt.z)
        self.cam.beginHUD()
        self.app.ellipse(x,y,5,5)
        self.cam.endHUD()
        
        '''
        self.app.pushMatrix()
        self.app.translate(pt.x,pt.y,pt.z);
        sphere(10);
        self.app.popMatrix()
        
        #self.app.point(pt.x,pt.y,pt.z)
        '''

    def _drawMesh(self, mesh):
        for v in mesh.pts: 
            pass
        for f in mesh.faces: 
            pass
            
        return True
        
    def _drawLinearEntity(self, ln):
        if ln._vec.length == 0 : return False
        
        if isinstance(ln, Segment) : 
            self.app.line(ln.spt.x,ln.spt.y,ln.spt.z,ln.ept.x,ln.ept.y,ln.ept.z)
            return True
        if isinstance(ln, Ray) : 
            return True
        if isinstance(ln, Line) : 
            return True

    def _drawPline(self, pline):
        return True
             
    def _drawPGon(self, rgon):
        self.app.beginShape()
        for pt in rgon.pts: self.app.vertex(pt.x,pt.y)
        self.app.endShape(CLOSE)
             
    def _drawCS(self, cs):
        return True
        
    def _drawCylCS(self, cs):
        return True


