import decodes.core as dc
from decodes.core import *
import math


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

    def get_polygons(self, bin_filled = Color(1), bin_edges = Color(.5)):
        if isinstance(self.filled, PGon):
            poly = self.filled
            poly.set_color(bin_filled)
            return [poly]
        if len(self.filling) == 0:
            e_list = []
            if bin_edges != None:
                for i in range(0,4):
                    e = Segment(self.boundary.corners[i],self.boundary.corners[(i+1)%4])
                    e.set_color(bin_edges)
                    e.set_weight(1)
                    e_list.append(e)
            return e_list
        p_list = []
        for j in range(len(self.filling)) :
            if bin_edges != None:
                for i in range(0,4):
                    e = Segment(self.boundary.corners[i],self.boundary.corners[(i+1)%4])
                    e.set_color(bin_edges)
                    e.set_weight(1)
                    p_list.append(e)
            p = self.filling[j].get_polygons(bin_filled, bin_edges)
            if p is not None: p_list.extend(p)
        return p_list



def sort_polygons(shapes = [], sort_type = 'w', reverse_list = False):
        """Sorts polygons into Bins.
            :param sort_type: how to sort polygons:
            :               'width' or 'w'  sort based on width
            :               'height' or 'h' sort based on height
            :               'area' or 'a'   sort based on area
            :               'ratio' or 'r'  sort based on aspect ratio
            :type sort_type: string   
        """

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

        return shapes

def bin_polygons(shapes = [], sheet_size = Interval(100,100)):
        """Places sorted polygons into Bins.
            :param shapes   : polygons to be placed
            :type shapes    : list of polygons   
            :returns        : Bins with the polygons within them
            :rtype          : list of Bins
        """

        # initialize
        sheets = [Bin(Point(0,0), sheet_size.a, sheet_size.b)]
        no_sheets = 1

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

        return sheets


def extract_polygons(sheets = [], border_color = Color(.75), bin_filled = Color(0), bin_edges = Color(.5)):
        """Creates a list of polygons that represents polygons and/or Bins.
            :param sheets: bins with polygons
            :type sheets : list
            :param border : color of sheets borders (or None)
            :type border : Color
            :returns: list of edges and polygons
            :rtype: list
        """ 
        # create list
        out_list = []
        for j,s in enumerate(sheets):
            out_list.extend(s.get_polygons(bin_filled, bin_edges))
            if border_color != None:
                border = PGon(s.boundary.corners).edges
                for b in border:
                    b.set_color(border_color)
                    b.set_weight(3)
                out_list.append(b)

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
