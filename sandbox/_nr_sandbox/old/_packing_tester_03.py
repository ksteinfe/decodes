import decodes as dc
from decodes.core import *
import random
from time import time

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack_09_"
random.seed(0)


class Bin():

    def __init__(self, cpt, w, h, filled = False, div_type = 'n'):
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

    def put_item(self, box):        
        result = [Bin(self.cpt, box.dim_x, box.dim_y, filled = True)]
        rem_x = self.boundary.dim_x - box.dim_x
        rem_y = self.boundary.dim_y - box.dim_y
        if rem_x <= 0: 
            if rem_y > 0 :result.append(Bin(self.cpt + Vec(0,box.dim_y), self.boundary.dim_x, rem_y))
        elif rem_y <= 0: result.append(Bin(self.cpt + Vec(box.dim_x,0), rem_x, self.boundary.dim_y))
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
                result.append(Bin(self.cpt + Vec(box.dim_x,0), rem_x, box.dim_y))
                result.append(Bin(self.cpt + Vec(0,box.dim_y), self.boundary.dim_x, rem_y))
            if divide_h :
                result.append(Bin(self.cpt + Vec(box.dim_x,0), rem_x, self.boundary.dim_y))
                result.append(Bin(self.cpt + Vec(0,box.dim_y), box.dim_x, rem_y))
        self.filling = result

    def can_fit(self, box):
        #full bin?
        if len(self.filling) == 0:
            if (box.dim_x <= self.w) and (box.dim_y <= self.h): return self
        else:
            for i in range(1,len(self.filling)) :
                result = self.filling[i].can_fit(box)
                if  result<> None : return result
        return None

    def get_polygons(self):
        if self.filled:

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
        # put shapes into list of Bounds objects
        b_list = [s.bounds for s in shapes]

        # create value field
        for i,b in enumerate(b_list):
            b.p_list = i
            if sort_type == 'w' : b.val = b.dim_x
            if sort_type == 'h' : b.val = b.dim_y
            if sort_type == 'a' : b.val = b.dim_x * b.dim_y
            if sort_type == 'r' :
                if b.dim_y != 0 : b.val = b.dim_x / b.dim_y
                else: b.val = 0

        # sort list
        b_list.sort(key=lambda b: (b.val), reverse=reverse_list)

        # initialize
        sheets = [Bin(Point(0,0), sheet_size.a, sheet_size.b)]

        for i, r in enumerate(b_list):
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
                sheets.append(Bin(Point(0,0), sheet_size.a, sheet_size.b))
                sheets[-1].put_item(r)
                print "adding bin ", len(sheets)-1

        # create files
        for j,s in enumerate(sheets):
            s.write_svg(f_prefix+'%03d'%j, path)

        # return list
        return b_list


# initialize parameters
sheet_size = Interval(960,480)
no_rects = 5

rect = []
for i in range(no_rects):
    if random.random() > .75:
        r_size = Interval(random.randrange(20,sheet_size.a,10), random.randrange(20,sheet_size.b,10))
    else:
        r_size = Interval(random.randrange(20,sheet_size.a/10,10), random.randrange(20,sheet_size.b/10,10))
    if r_size.is_ordered : r_size = Interval(r_size.b, r_size.a)
    rect.append(PGon.rectangle(Point(0,0), r_size.a, r_size.b))

new_list = bin_polygons(rect,sheet_size, 'r', reverse_list = True)

for n,i in enumerate(new_list):
    print 'item ',n,' : = ',i.dim_x,", ",i.dim_y

    
raw_input("press enter...")
stop   
            
         

# initialize parameters
sheet_size = Interval(960,480)
no_rects = 100

rect = []
for i in range(no_rects):
    if random.random() > .75:
        r_size = Interval(random.randrange(20,sheet_size.a,10), random.randrange(20,sheet_size.b,10))
    else:
        r_size = Interval(random.randrange(20,sheet_size.a/10,10), random.randrange(20,sheet_size.b/10,10))
    if r_size.is_ordered : r_size = Interval(r_size.b, r_size.a)
    rect.append(Bounds(center=Point(0,0), dim_x = r_size.a, dim_y = r_size.b))

# sort them by width
a = rect
rect.sort(key=lambda r: (r.dim_x), reverse=True)

# initialize
sheets = [Bin(Point(0,0), sheet_size.a, sheet_size.b)]

for i, r in enumerate(rect):
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
        sheets.append(Bin(Point(0,0), sheet_size.a, sheet_size.b))
        sheets[-1].put_item(r)
        print "adding bin ", len(sheets)-1

# create files
for j,s in enumerate(sheets):
    s.write_svg(f_prefix+'%03d'%j, path)



'''
the_rect = PGon.rectangle(Point(0,0),50.0,70.0)


test = Bin(Point(0,0), 500.0,500.0)


test.put_item(the_rect)

new_bin = test.can_fit(the_rect)

if new_bin <> None:
    new_bin.put_item(the_rect)


test.write_svg(f_prefix, path)
'''





raw_input("press enter...")