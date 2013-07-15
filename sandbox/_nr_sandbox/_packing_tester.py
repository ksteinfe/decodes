import decodes as dc
from decodes.core import *
from decodes.extensions.reaction_diffusion import GrayScott
import random
from time import time

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack"
random.seed(0)


class Bin():

    def __init__(self, cpt, w, h, filled = 'open'):

        self.cpt = cpt
        self.w = w
        self.h = h
        self.filled = filled
        self.boundary = PGon.rectangle(Point(cpt.x+w/2.0, cpt.y+h/2.0), w, h)
        self.filling = []

    def put_item(self, rect):
        size = rect[2] - rect[0]
        result = [Bin(self.cpt, size.x,size.y, 'filled')]
        if self.w > size.x: result.append(Bin(self.cpt + Vec(size.x,0), self.w - size.x, size.y))
        if self.h > size.y: result.append(Bin(self.cpt + Vec(0,size.y), size.x, self.h - size.y))
        self.filling = result

    def can_fit(self, rect):
        #full bin?
        if len(self.filling) == 0:
            size = rect[2] - rect[0]
            if (size.x <= self.w) and (size.y <= self.h): return self
        else:
            for i in range(1,len(self.filling)) :
                result = self.filling[i].can_fit(rect)
                if  result<> None : return result
        return None

    def svg_code(self):
        if self.filled == 'filled':
            point_string = " ".join([str(v.x)+","+str(v.y) for v in self.boundary.pts])
            style = 'fill:rgb(120,120,120);stroke-width:1;stroke:rgb(0,0,0)'
            atts = 'points="'+point_string+'"'
            return '<polygon '+atts+' style="'+style+'"/>\n'
        if len(self.filling) == 0:
            return ''
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

        # write outline of sheet
        point_string = " ".join([str(v.x)+","+str(v.y) for v in self.boundary.pts])
        style = 'fill:rgb(255,255,255);stroke-width:3;stroke:rgb(0,0,0)'
        atts = 'points="'+point_string+'"'
        buffer.write('<polygon '+atts+' style="'+style+'"/>\n')

        #write filled pieces
        svg_code = self.svg_code()
        buffer.write(svg_code)


        buffer.write('</svg>')

        # write buffer to file
        fo = open(filepath, "wb")
        fo.write( buffer.getvalue() )
        fo.close()
        buffer.close()



# initialize parameters
sheet_size = Interval(960,480)
no_rects = 30

rect = []
for i in range(no_rects):
    r_size = Interval(random.randrange(20,100,10), random.randrange(20,100,10))
    if r_size.is_ordered : r_size = Interval(r_size.b, r_size.a)
    rect.append(PGon.rectangle(Point(0,0), r_size.a, r_size.b))

# sort them by width
a = rect
rect.sort(key=lambda r: (r.edges[0].length), reverse=True)

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