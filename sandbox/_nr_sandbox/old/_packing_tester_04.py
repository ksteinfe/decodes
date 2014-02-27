import decodes as dc
from decodes.core import *
import random
from time import time
import math

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack_17_"
random.seed(0)


class Bin():

    def __init__(self, cpt, w, h, filled = False, div_type = 'a'):
        """Creates a Bin object that contains filled areas and open sub-bins.
        
            :param cpt: Corner point
            :type cpt: Point
            :param w: Width of Bin
            :type w: float
            :param h: Height of Bin
            :type h: float
            :param filled: Is this Bin currently filled?
            :type filled: boolean
            :param div_type: how to divide Bin object:
            :               'width' or 'w'  make sub-Bin with largest width
            :               'height' or 'h' make sub-Bin with largest height
            :               'area' or 'a'   make sub-Bin with largest area
            :               'max' or 'x'    make sub-Bin with maximum aspect ratio
            :               'min' or 'n'    make sub-Bin with minimum aspect ratio
            :type div_type: string       
        """

        self.cpt = cpt
        self.w = w
        self.h = h
        self.filled = filled
        self.div = div_type
        self.boundary = Bounds(center = Point(cpt.x+w/2.0, cpt.y+h/2.0), dim_x =w, dim_y = h)
        self.filling = []

    def put_item(self, shape):     
        c = CS(self.cpt - shape.bounds.corners[0])
        shape.basis = c   
        result = [Bin(self.cpt, shape.bounds.dim_x, shape.bounds.dim_y, filled = shape)]
        rem_x = self.boundary.dim_x - shape.bounds.dim_x
        rem_y = self.boundary.dim_y - shape.bounds.dim_y
        if rem_x <= 0: 
            if rem_y > 0 :result.append(Bin(self.cpt + Vec(0,shape.bounds.dim_y), self.boundary.dim_x, rem_y))
        elif rem_y <= 0: result.append(Bin(self.cpt + Vec(shape.bounds.dim_x,0), rem_x, self.boundary.dim_y))
        else:
            divide_w = False
            divide_h = False
            if self.div == 'w' : divide_w = True
            if self.div == 'h' : divide_h = True
            if self.div == 'a' :
                divide_w = ((self.boundary.dim_x * rem_y) > (rem_x * self.boundary.dim_y))
                divide_h = not(divide_w)
            if self.div == 'n':
                divide_w = ((self.boundary.dim_x / rem_y) < (self.boundary.dim_y / rem_x))
                divide_h = not(divide_w)
            if self.div == 'x':
                divide_w = ((self.boundary.dim_x / rem_y) > (self.boundary.dim_y / rem_x))
                divide_h = not(divide_w)
            if divide_w :
                result.append(Bin(self.cpt + Vec(shape.bounds.dim_x,0), rem_x, shape.bounds.dim_y))
                result.append(Bin(self.cpt + Vec(0,shape.bounds.dim_y), self.boundary.dim_x, rem_y))
            if divide_h :
                result.append(Bin(self.cpt + Vec(shape.bounds.dim_x,0), rem_x, self.boundary.dim_y))
                result.append(Bin(self.cpt + Vec(0,shape.bounds.dim_y), shape.bounds.dim_x, rem_y))
        self.filling = result

    def can_fit(self, shape):
        #full bin?
        if len(self.filling) == 0:
            if (shape.bounds.dim_x <= self.w) and (shape.bounds.dim_y <= self.h): return self
        else:
            for i in range(1,len(self.filling)) :
                result = self.filling[i].can_fit(shape)
                if  result<> None : return result
        return None

    def get_polygons(self):
        if isinstance(self.filled, PGon):
            return [self.filled]
        if len(self.filling) == 0:
            e_list = []
            for i in range(0,4):
                e = Segment(self.boundary.corners[i],self.boundary.corners[(i+1)%4])
                e.set_color(.5,.5,.5)
                e.set_weight(1)
                e_list.append(e)
            return e_list
        p_list = []
        for j in range(len(self.filling)) :
            for i in range(0,4):
                e = Segment(self.boundary.corners[i],self.boundary.corners[(i+1)%4])
                e.set_color(.5,.5,.5)
                e.set_weight(1)
                p_list.append(e)
            p = self.filling[j].get_polygons()
            if p is not None: p_list.extend(p)
        return p_list


    def svg_code(self):
        if self.filled:
            point_string = " ".join([str(v.x)+","+str(v.y) for v in self.boundary.corners])
            style = 'fill:rgb(120,120,120);stroke-width:1;stroke:rgb(0,0,0)'
            atts = 'points="'+point_string+'"'
            return '<polygon '+atts+' style="'+style+'"/>\n'
        if len(self.filling) == 0:
            point_string = " ".join([str(v.x)+","+str(v.y) for v in self.boundary.corners])
            style = 'fill:rgb(255,255,255);stroke-width:.5;stroke:rgb(128,128,128)'
            atts = 'points="'+point_string+'"'
            return '<polygon '+atts+' style="'+style+'"/>\n'
        code = ''
        for i in range(len(self.filling)) :
            code = code + self.filling[i].svg_code()
        return code

    def write_svg(self,f_name="svg_out", f_path= os.path.expanduser("~"), cdim=Interval(500,500), color_dict = {0:Color(0.0),1:Color(1.0)}):
        # quick and dirty svg writer
        cdim = Interval(self.w,self.h)
        ht = cdim.b
        filepath = f_path + os.sep + f_name+".svg"

        c = min(cdim.a/self.w,cdim.b/self.h)
        print "drawing svg to "+filepath

        buffer = cStringIO.StringIO()
        svg_size = ""
        svg_size = 'width="'+str(cdim.a)+'" height="'+str(cdim.b)+'"'

        buffer.write('<svg '+svg_size+' xmlns="http://www.w3.org/2000/svg" version="1.1">\n')

        #write filled pieces
        svg_code = self.svg_code()
        buffer.write(svg_code)

        # write outline of sheet
        point_string = " ".join([str(v.x)+","+str(v.y) for v in self.boundary.corners])
        style = 'fill:none;stroke-width:3;stroke:rgb(0,0,0)'
        atts = 'points="'+point_string+'"'
        buffer.write('<polygon '+atts+' style="'+style+'"/>\n')

        buffer.write('</svg>')

        # write buffer to file
        fo = open(filepath, "wb")
        fo.write( buffer.getvalue() )
        fo.close()
        buffer.close()


def bin_polygons(shapes = [], sheet_size = Interval(100,100),sort_type = 'w', reverse_list = False):
        """Creates a sorted list of polygons.
            :param sort_type: how to sort polygons:
            :               'width' or 'w'  sort based on width
            :               'height' or 'h' sort based on height
            :               'area' or 'a'   sort based on area
            :               'ratio' or 'r'  sort based on aspect ratio
            :type sort_type: string   
        """
        global no_sheets

        # create value field
        for i,s in enumerate(shapes):
            if sort_type == 'w' : s.val = s.bounds.dim_x
            if sort_type == 'h' : s.val = s.bounds.dim_y
            if sort_type == 'a' : s.val = s.bounds.dim_x * s.bounds.dim_y
            if sort_type == 'r' :
                if s.bounds.dim_y != 0 : s.val = s.bounds.dim_x / s.bounds.dim_y
                else: s.val = 0

        # sort list
        shapes.sort(key=lambda s: (s.val), reverse=reverse_list)

        # initialize
        sheets = [Bin(Point(0,0), sheet_size.a, sheet_size.b)]
        #no_sheets = 1

        for i, r in enumerate(shapes):
            # see if rectangle fits into one of the sheets
            print "looking at item ",i
            flag = False
            for j, s in enumerate(sheets):
                test_bin = s.can_fit(r)
                if test_bin <> None:
                    test_bin.put_item(r)
                    print "packing into bin ",j
                    flag = True
                    break
            # if we get here we have not placed the rectangle
            # so we need to add a new one
            if not flag:
                sheets.append(Bin(Point(no_sheets*sheet_size.a,0), sheet_size.a, sheet_size.b))
                no_sheets += 1
                sheets[no_sheets-1].put_item(r)
                print "adding bin ", no_sheets-1

        # create files
        #for j,s in enumerate(sheets):
        #    s.write_svg(f_prefix+'%03d'%j, path)

        # create list
        out_list = []
        for j,s in enumerate(sheets):
            out_list.extend(s.get_polygons())
            border = PGon(s.boundary.corners).edges
            for b in border:
                b.set_color(.5,.5,.5)
                b.set_weight(3)
            out_list.append(border)

        # return list
        return out_list

def rand_points(n,size):
    r_int = Interval.twopi()

    r_ints = r_int.rand_interval(n)
    pts = []
    for i in range(n):
        dist = random.uniform(1,size)
        pts.append(CylCS().eval(dist, r_ints[i].b))
    return pts

# initialize parameters
print rand_points(10,100)

sheet_size = Interval(240,240)
no_rects = 40
no_sheets = 1

shapes = []
for i in range(no_rects):
    shapes.append(PGon(rand_points(random.randint(3,10),random.randint(1,min(sheet_size.a,sheet_size.b)/3))))

new_list = bin_polygons(shapes,sheet_size, 'w', reverse_list = True)


#for n,i in enumerate(new_list):
#    print 'item ',n,' : = ',i.pts


outie = dc.makeOut(dc.Outies.SVG, f_prefix, canvas_dimensions=Interval(no_sheets * sheet_size.a,sheet_size.b), flip_y = True)
scale = 1

for x in new_list:
    outie.put(x)
    
outie.draw()
    
raw_input("press enter...")