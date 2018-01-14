from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_curve
if VERBOSE_FS: print("surface.py loaded")



class Surface(IsParametrized):
    """
    A simple surface class

    To construct a surface, pass in a function and [optionally] two intervals that determine the a valid range of u&v values.
    
    The function should expect two parameters u and v (float), and return a Point.

    """
    
    def __init__(self, function=None, dom_u=Interval(0,1), dom_v=Interval(0,1), tol_u=None, tol_v=None):
        """ Constructs a Curve object. If tolerance is None, Curve.tol = tol_max().
        
            :param function: A function returning points.
            :type function: function
            :param dom_u: Domain for u-value of curve points.
            :type dom_u: Interval
            :param dom_v: Domain for v-value of curve points.
            :type dom_v: Interval
            :param tol_u: The tolerance of u-direction of this Surface expressed in domain space.
            :type tol_u: float
            :param tol_v: The tolerance of v-direction of this Surface expressed in domain space.
            :type tol_v: float
            :result: Surface object.
            :rtype: Surface
            
            ::
            
                def func(u,v):
                    return Point(u,v)
                Int=Interval(1,20)
                my_surf=Surface(func,Int,Int)
        """
        if function is not None : self._func = function
        self._dom = dom_u, dom_v
        self._tol = self.tol_max
        if tol_u is not None : self.tol_u = tol_u
        if tol_v is not None : self.tol_v = tol_v

        for u,v in [(self.u0,self.v0),(self.u0,self.v1),(self.u1,self.v1),(self.u1,self.v0)]:
            try:
                pt = self.func(u,v)
                pt.x
                pt.y
                pt.z
            except:
                raise GeometricError("Surface not valid: The given function does not return a point at parameter %s, %s"%(u,v))
                    


    @property
    def surrogate(self):
        """Returns a mesh copy of this surface.
        
            :result: Mesh copy of this surface.
            :rtype: Mesh
            
            ::
                
                my_surf.surrogate
            
        """
        
        try:
            return self._surrogate
        except:
            self._surrogate = self.to_mesh()
            return self._surrogate

    def _rebuild_surrogate(self):
        """Deletes attributes of this surrogate Surface.
        
            :result: None
            :rtype: None
            
        """
    
        try: delattr(self, "_surrogate")
        except:
            pass


    @property
    def domain_u(self): 
        """Returns the Interval domain for the U-direction of this Surface.
            
            :result: Domain of this Surface in the U-direction.
            :rtype: Interval
        """
        return self._dom[0]

    @property
    def u0(self):
        """Returns the minimum value for the U domain of this Surface.
            
            :result: Minimum value for U domain.
            :rtype: float
            
        """
        return self._dom[0].a

    @property
    def u1(self):
        """Returns the maximum value for the U domain of this Surface.
        
            :result: Maximum value for U domain.
            :rtype: float
            
        """
        return self._dom[0].b

    @property
    def v0(self):
        """Returns the minimum value for the V domain of this Surface.
        
            :result: Minimum value for V domain.
            :rtype: float
            
        """
        return self._dom[1].a

    @property
    def v1(self):
        """Returns the maximum value for the V domain of this Surface.
        
            :result: Maximum value for V domain.
            :rtype: float
        
        """
        return self._dom[1].b

    @property
    def domain_v(self): 
        """Returns the Interval domain for the V-direction of this Surface.
           
            :result: Domain of this Surface in the V-direction.
            :rtype: Interval
            
        """
        return self._dom[1]

    @property
    def tol_max(self):
        """Determines the maximum tolerance as Surface.domain_u.delta / 10 , Surface.domain_v.delta / 10.
        
            :result: [Maximum U-tolerance, Maximum V-tolerance]
            :rtype: [float, float]
        """
        return [self._dom[0].delta / 10.0, self._dom[1].delta / 10.0]

    @property
    def tol_u(self):
        """Returns tolerance in the U-direction of this Surface.
        
            :result: Tolerance in U-direction.
            :rtype: float
            
        """
        return self._tol[0]

    @tol_u.setter
    def tol_u(self, tolerance):
        """Sets the tolerance of this Surface in the U-direction.
            
            :param tolerance: Tolerance of this Surface.
            :type tolerance: float
            :result: None
            :rtype: None
            
        """
        self._tol[0] = tolerance
        if self._tol[0] > self.tol_max[0] :  
            warnings.warn("Surface u tolerance too high relative to u domain - Resetting to max tol.  tol_u (%s) > Surface.max_tol(%s)"%(tolerance,self.tol_max))
            self._tol[0] = self.tol_max[0]
        self._rebuild_surrogate()

    @property
    def tol_u_nudge(self):
        return self.tol_u/100.0

    @property
    def tol_v(self):
        """Returns the tolerance of this Surface in the V-direction.
        
            :result: Tolerance in V-direction.
            :rtype: float
            
        """
        return self._tol[1]

    @tol_v.setter
    def tol_v(self, tolerance):
        """Sets the tolerance of this surface in the V-direction.
        
            :param tolerance: Tolerance of this Surface.
            :type tolerance: float
            :result: None
            :rtype: None
        """
        self._tol[1] = tolerance
        if self._tol[1] > self.tol_max[1] :  
            warnings.warn("Surface v tolerance too high relative to v domain - Resetting to max tol.  tol_v (%s) > Surface.max_tol(%s)"%(tolerance,self.tol_max))
            self._tol[1] = self.tol_max[1]
        self._rebuild_surrogate()

    @property
    def tol_v_nudge(self):
        return self.tol_v/100.0


    def deval(self,u,v):
        """| Evaluates this Surface and returns a Point.
           | u and v are float values that fall within the defined domain of this Surface.

           :param u: U-value to evaluate the Surface at.
           :type u: float
           :param v: V-value to evaluate the Surface at.
           :type v: float
           :result: a Point on this Surface.
           :rtype: Point
            
           ::
            
               my_surf.deval(5,5)
        """
        '''
        # some rounding errors require something like this:
        if u < self.u0 and u > self.u0-self.tol_u : u = u0
        if u > self.u1 and u < self.u1+self.tol_u : u = u1
        if v < self.v0 and v > self.v0-self.tol_v : v = v0
        if v > self.v1 and v < self.v1+self.tol_v : v = v1
        '''
        if u not in self.domain_u : raise DomainError("Surface evaluated outside the bounds of its u-domain: deval(%s) %s"%(u,self.domain_u))
        if v not in self.domain_v : raise DomainError("Surface evaluated outside the bounds of its v-domain: deval(%s) %s"%(v,self.domain_v))
        
        return Point(self.func(u,v))


    def deval_pln(self,u,v):
        """| Evaluates this Surface and returns a Plane.
           | u and v are float values that fall within the defined domain of this Surface.
           | Tangent vector determined by a nearest neighbor at distance Surface.tol/100

           :param u: U-value to evaluate the Surface at.
           :type u: float
           :param v: V-value to evaluate the Surface at.
           :type v: float
           :result: a Plane on this Surface.
           :rtype: Plane
           
           ::
                
               my_surf.deval_pln(5,5)
        """
        '''
        # some rounding errors require something like this:
        if u < self.u0 and u > self.u0-self.tol_u : u = u0
        if u > self.u1 and u < self.u1+self.tol_u : u = u1
        if v < self.v0 and v > self.v0-self.tol_v : v = v0
        if v > self.v1 and v < self.v1+self.tol_v : v = v1
        '''
        if u not in self.domain_u : raise DomainError("Surface evaluated outside the bounds of its u-domain: deval(%s) %s"%(u,self.domain_u))
        if v not in self.domain_v : raise DomainError("Surface evaluated outside the bounds of its v-domain: deval(%s) %s"%(v,self.domain_v))

        pt,vec_u,vec_v = self._nudged(u,v)
        vec = vec_u.cross(vec_v)

        return Plane(pt, vec)
        


    def deval_curviso(self,u,v,calc_extras=False):
        """Calculates the curvature of this Surface at a given location.
        
            :param u: U-value to evaluate the Surface at.
            :type u: float
            :param v: V-value to evaluate the Surface at.
            :type v: float
            :param calc_extras: Boolean value.
            :type calc_extras: bool
            :result: (Curvature at point in U-direction, osculating Circle), (Curvature at point in V-direction, osculating Circle)
            :rtype: (float, Circle), (float, Circle)
            
            ::
            
                my_surf.deval_curviso(3,5)
            
        """
        # calculates the curvature of the isoparms of this surfaces
        # returns curvature values and osc circles
        pt, u_pos, u_neg, v_pos, v_neg = self._nudged(u,v,True)

        # if given a surface edge, nudge vectors a bit so we don't get zero curvature, but leave origin the same
        if (u-self.tol_u_nudge <= self.domain_u.a):
            nudged = self._nudged(self.tol_u_nudge,v,True)
            u_pos = nudged[1]
            u_neg = nudged[2]
        if (u+self.tol_u_nudge >= self.domain_u.b):
            nudged = self._nudged(self.domain_u.b-self.tol_u_nudge,v,True)
            u_pos = nudged[1]
            u_neg = nudged[2]

        if (v-self.tol_v_nudge <= self.domain_v.a):
            nudged = self._nudged(u,self.tol_v_nudge,True)
            v_pos = nudged[3]
            v_neg = nudged[4]
        if (v+self.tol_v_nudge >= self.domain_v.b):
            nudged = self._nudged(u,self.domain_v.b-self.tol_v_nudge,True)
            v_pos = nudged[3]
            v_neg = nudged[4]

        crv_u = Curve._curvature_from_vecs(pt,u_pos,u_neg,calc_extras)
        crv_v = Curve._curvature_from_vecs(pt,v_pos,v_neg,calc_extras)
        
        if calc_extras : return crv_u[0]*crv_v[0], (crv_u[0],crv_v[0]),(crv_u[1],crv_v[1])
        return crv_u,crv_v

    def deval_curv(self,u,v,calc_extras=False):
        """ IN:  
        
            - a point u,v (given on this surface domain) referring to a point on the surface.

            OUT:
        
            The following geometric entities describing the shape of the surface at a given point:
        
            - principal directions (expressed as a coordinate system)
        
            - curvatures: principal curvatures (min/max), Gaussian curvature (K), Mean Curvature (H)

            Note: All quantities at a given point are computed using nearest neighbors on a mesh.  
        
            For the case of a parametrized surface, we take a mesh of nearest neighbors with vertices given by the isocurves at a resolution tol_nudge. These calculations are good for any mesh on a surface;  all that would need to change for another type of mesh is: 
        
                (1) the construction of the mesh of nearest neighbors around the surface point in question 
        
                (2) the calculation of the areas of the faces and the weighted face areas
        
            ref: 
        
            Taubin, Gabriel, Estimating the Tensor of Curvature of a Surface from a Polyhedral
        
            Approximation, http://pdf.aminer.org/000/234/737/curvature_approximation_for_triangulated_surfaces.pdf

            Note: We can define projection onto a surface by computing the normal on the surrogate.
        
            :param u: U-value to evaluate Surface at.
            :type u: float
            :param v: V-value to evaluate Surface at.
            :type v: float
            :param calc_extras: Boolean value.
            :type calc_extras: bool
            :result: The principal directions (CS), minimum curvature, maximum curvature, Gaussian curvature, Mean curvature
            :rtype: CS, float, float, float, float
            
            ::
            
                my_surf.deval_curv(5,4)
            
        """
        # * eliminate when we have a matrix class or can import numpy
        def matrix_mult(matrix1,matrix2):
            if len(matrix1[0]) != len(matrix2):
                print("Matrices can't be multiplied!")
            else:
                m = len(matrix1)
                n = len(matrix1[0])
                p = len(matrix2[0])
                new_matrix = [[0 for row in range(p)] for col in range(m)]
                for i in range(m):
                    for j in range(p):
                        for k in range(n):
                            new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
                return new_matrix

        ret = []
        pt_uv = self.func(u,v)
        ret.append(pt_uv)

        #construct mesh of nearest neighbors, with 0 indexing p_uv and neighbors indexed counter clockwise. 
        ngbr = Mesh()
        pt, u_pos, u_neg, v_pos, v_neg = self._nudged(u,v,True)
        ngbr.append(pt_uv)
        ngbr.append(pt_uv +  u_pos )
        ngbr.append(pt_uv +  u_pos  +  v_pos)
        ngbr.append(pt_uv +  v_pos )
        ngbr.append(pt_uv +  u_neg  +  v_pos)
        ngbr.append(pt_uv +  u_neg )
        ngbr.append(pt_uv +  u_neg  +  v_neg)
        ngbr.append(pt_uv +  v_neg )
        ngbr.append(pt_uv +  u_pos  +  v_neg)
    
        #Triangular mesh
        ngbr.add_face(0,1,2)
        ngbr.add_face(0,2,3)
        ngbr.add_face(0,3,5)
        ngbr.add_face(0,5,6)
        ngbr.add_face(0,6,7)
        ngbr.add_face(0,7,1)

        #weights stores the sum of the face areas for faces touching at given vertex and p_uv
        #used for creating the matrix needed for the calculation of the principals
        weights = [0]*len(ngbr) 

        #Compute the normal vector and tangent plane at the point pt_uv
        N_vec = Vec(0,0,0)
        for k in range(len(ngbr.faces)):
            verts = ngbr.face_pts(k)
            face_area = 0.5*Vec(verts[0],verts[1]).cross(Vec(verts[0],verts[2])).length #Triangular face area
            N_vec = N_vec + ngbr.face_normal(k)*face_area
            for i in ngbr.faces[k]:
                weights[i] += face_area
        N_vec = N_vec.normalized()
        tangent_plane = Plane(pt_uv, N_vec)

        #Compute the principal curvatures and directions at the point pt_uv (*)

        #Form the matrix needed for the calculation of the principal curvatures/directions
        M_mat = [[0 for row in range(3)] for col in range(3)]
        weights_sum = sum(weights)
        for k in range(1,len(ngbr)):
            vec_k = Vec(ngbr[k] - pt_uv) 
            #T_k is normalized projecton of vec_k onto the tangent plane
            T_k = (vec_k - N_vec*(vec_k.dot(N_vec))).normalized().to_tuple()
            #kappa_k is the approximate directional curvature at ngbr[k]
            kappa_k = 2*N_vec.dot(vec_k)/vec_k.length2
            w_k =  weights[k]/weights_sum
            factor = kappa_k*w_k  
            for row in range(3):
               for col in range(3):
                   M_mat[row][col] += factor * T_k[row] * T_k[col]
 
        """
        #Check that N_vec is an eigenvector of M_mat (with eigenvalue 0)
        N = [[N_vec.x], [N_vec.y], [N_vec.z]]
        print matrix_mult(M_mat, N)
        """

        #Form matrix for Householder transformation(reflection matrix Q = I - 2*W*transpose(W))
        E_vec = Vec(1,0,0)
        if (E_vec - N_vec).length2 > (E_vec + N_vec).length2:
            W_vec = (Vec(1,0,0) - N_vec).normalized().to_tuple()
        else:
            W_vec = (Vec(1,0,0) + N_vec).normalized().to_tuple()
    
        I_mat = [[1,0,0], [0,1,0], [0,0,1]] 
        Q_mat = [[0 for row in range(3)] for col in range(3)]

        for row in range(3):
            for col in range(3):
                Q_mat[row][col] = I_mat[row][col] - 2 * W_vec[row] * W_vec[col]

        """
        #Check that +- N_vec is the first column of Q
        print N_vec, Q_mat
        """

        T1_tilde = Vec(Q_mat[0][1], Q_mat[1][1], Q_mat[2][1])
        T2_tilde = Vec(Q_mat[0][2], Q_mat[1][2], Q_mat[2][2])
        """
        #Check that these vectors are orthonormal
        print T1_tilde.length, T2_tilde.length, T1_tilde.dot(T2_tilde)
        """

        #Apply Householder transformation by forming matrix : transpose(Q)*M*Q = Q*M*Q
        #Note: Q_mat_transpose = transpose(Q_mat)
        M_s =  matrix_mult(matrix_mult(Q_mat, M_mat), Q_mat)
        m11 = M_s[1][1]
        m12 = M_s[1][2]
        m21 = M_s[2][1]
        m22 = M_s[2][2]
        M_s_restricted = [[m11, m12],[m21 , m22]]

        """
        #Check that M_s_rectricted (restriction of M_s on tangent space) is symmetric
        print "Matrix to be diagonalized", M_s_restricted
        """

        #Calculate the Givens rotation angle
        theta = 0.5*math.atan2(2*m12, m22-m11)
        cos = math.cos(theta)
        sin = math.sin(theta)

        """
        #Check that transpose(Rot)*M_s_restricted*Rot is diagonal
        Rot_mat = [[cos, sin],[-sin, cos]]
        print matrix_mult(matrix_mult(transpose(Rot_mat), M_s_restricted), Rot_mat)
        """

        #Calculate the eigenvectors and eigenvalues of M_mat
        T1_vec = T1_tilde*cos - T2_tilde*sin
        T2_vec = T1_tilde*sin + T2_tilde*cos
        d1 = cos*cos*m11 - 2*cos*sin*m12 + sin*sin*m22 
        d2 = sin*sin*m11 + 2*cos*sin*m12 + cos*cos*m22

        if d1 > d2:
            d1,d2 = d2,d1
            T1_vec, T2_vec = T2_vec, T1_vec

        """
        #Check that T1, T2 are eigenvectors of M_mat
        T1 = [[T1_vec.x], [T1_vec.y], [T1_vec.z]]
        T2 = [[T2_vec.x], [T2_vec.y], [T2_vec.z]]
        T1_test = matrix_mult(M_mat, T1)
        #These should all equal d1
        print T1_test[0][0]/T1[0][0], T1_test[1][0]/T1[1][0], T1_test[2][0]/T1[2][0]
        T2_test = matrix_mult(M_mat, T2)
        #These should all equal d2
        print T2_test[0][0]/T2[0][0], T2_test[1][0]/T2[1][0], T2_test[2][0]/T2[2][0]
        """ 

        #T1 and T2 are the principal directions.  Form a coordinate system aligned with these directions.
        cs_principal = CS(pt_uv, T1_vec, T2_vec)

        #Compute all the curvature quantities: principal curvatures, Gaussian, Mean
        k1 = 3*d1 - d2
        k2 = 3*d2 - d1
        K = k1*k2
        H = (k1 + k2)*0.5
        if k1 == k2 : 
            if not calc_extras : return False
            return False, k1, k2, K, H

        if not calc_extras : return cs_principal
        return cs_principal, k1, k2, K, H

    def eval(self,u,v):
        """| Evaluates this Surface and returns a Point.
           | u and v are normalized float values (0->1) which will be remapped to the domain defined by this Surface.
           | Equivalent to Surface.deval(Interval.remap(t,Interval(),Surface.domain))
            
           :param u: U value to evaluate Surface at.
           :type u: float
           :param v: V value to evaluate Surface at.
           :type v: float
           :result: a Point on this Surface.
           :rtype: Point
        """
        if u<0 or u>1 : raise DomainError("u out of bounds.  eval() must be called numbers between 0->1: eval(%s)"%u)
        if v<0 or v>1 : raise DomainError("v out of bounds.  eval() must be called numbers between 0->1: eval(%s)"%v)
        return self.deval(Interval.remap(u,Interval(),self.domain_u),Interval.remap(v,Interval(),self.domain_v))

    def eval_pln(self,u,v):
        """| Evaluates this Curve and returns a Plane.
           | u and v are normalized float values (0->1) which will be remapped to the domain defined by this Surface.
           | Equivalent to Surface.deval(Interval.remap(t,Interval(),Surface.domain)).
            
           :param u: U value to evaluate the Surface at.
           :type u: float
           :param v: V value to evaluate the Surface at.
           :type v: float
           :result: a Plane on this Surface.
           :rtype: Plane
        """
        if u<0 or u>1 : raise DomainError("u out of bounds.  eval() must be called numbers between 0->1: eval(%s)"%u)
        if v<0 or v>1 : raise DomainError("v out of bounds.  eval() must be called numbers between 0->1: eval(%s)"%v)
        return self.deval_pln(Interval.remap(u,Interval(),self.domain_u),Interval.remap(v,Interval(),self.domain_v))

    def eval_curviso(self,u,v,calc_extras=False):
        """Calculates the curvature of this Surface at a given location.
        
            :param u: U-value to evaluate the Surface at.
            :type u: float
            :param v: V-value to evaluate the Surface at.
            :type v: float
            :param calc_extras: Boolean value.
            :type calc_extras: bool
            :result: (Curvature at point in U-direction, osculating Circle), (Curvature at point in V-direction, osculating Circle)
            :rtype: (float, Circle), (float, Circle)
            
        """
        if u<0 or u>1 : raise DomainError("u out of bounds.  eval_curvature() must be called numbers between 0->1: eval(%s)"%u)
        if v<0 or v>1 : raise DomainError("v out of bounds.  eval_curvature() must be called numbers between 0->1: eval(%s)"%v)
        return self.deval_curviso(Interval.remap(u,Interval(),self.domain_u),Interval.remap(v,Interval(),self.domain_v),calc_extras)

    def eval_curv(self,u,v,calc_extras=False):
        """ Returns the curvature of a surface at a given location u,v. Equivalent to deval_curv.
        
            :param u: U-value to evaluate Surface at.
            :type u: float
            :param v: V-value to evaluate Surface at.
            :type v: float
            :param calc_extras: Boolean value.
            :type calc_extras: bool
            :result: The principal directions (CS), minimum curvature, maximum curvature, Gaussian curvature, Mean curvature
            :rtype: CS, float, float, float, float
                        
        """
        if u<0 or u>1 : raise DomainError("u out of bounds.  eval_curvature() must be called numbers between 0->1: eval(%s)"%u)
        if v<0 or v>1 : raise DomainError("v out of bounds.  eval_curvature() must be called numbers between 0->1: eval(%s)"%v)
        return self.deval_curv(Interval.remap(u,Interval(),self.domain_u),Interval.remap(v,Interval(),self.domain_v),calc_extras)

    def _nudged(self,u,v,include_negs = False):
        """Returns the nearest neighbors along u and v axis of a point(u,v). Used for discrete approximations calculations.
        
            :param u: U value to evaluate the Surface at.
            :type u: float
            :param v: V value to evaluate the Surface at.
            :type v: float
            :param include_negs: Boolean value.
            :type include_negs: bool
            :result: Point, first U-direction Vec, second U-direction Vec, first V-direction Vec, second V-direction Vec
            :rtype: Point, Vec, Vec, Vec, Vec
            
        """
        #nearest neighbors along u and v axis of point(u,v); used for discrete approximations calculations 
        if u not in self.domain_u : raise DomainError("Surface evaluated outside the bounds of its u-domain: deval(%s) %s"%(u,self.domain_u))
        if v not in self.domain_v : raise DomainError("Surface evaluated outside the bounds of its v-domain: deval(%s) %s"%(v,self.domain_v))
        pt = Point(self.func(u,v))
        
        vec_u = False
        vec_ui = False
        if (u+self.tol_u_nudge <= self.domain_u.b): 
            vec_u = Vec(pt,self.func(u + self.tol_u_nudge,v))
        else:
            vec_ui = Vec(pt,self.func(u - self.tol_u_nudge,v))
            vec_u = vec_ui.inverted()

        vec_v = False
        vec_vi = False
        if (v+self.tol_v_nudge <= self.domain_v.b): 
            vec_v = Vec(pt,self.func(u,v + self.tol_v_nudge))
        else:
            vec_vi = Vec(pt,self.func(u,v - self.tol_v_nudge))
            vec_v = vec_vi.inverted()

        if not include_negs : return pt,vec_u,vec_v

        if not vec_ui: 
            if (u-self.tol_u_nudge >= self.domain_u.a): vec_ui = Vec(pt,self.func(u - self.tol_u_nudge,v))
            else : vec_ui = vec_u.inverted()
        if not vec_vi: 
            if (v-self.tol_v_nudge >= self.domain_v.a): vec_vi = Vec(pt,self.func(u,v - self.tol_v_nudge))
            else : vec_vi = vec_v.inverted()

        return pt,vec_u,vec_ui,vec_v,vec_vi


    def to_mesh(self,do_close=False,tris=False,divs_u=False,divs_v=False):
        """ Returns a mesh from this Surface.
        
            :param do_close: Boolean value.
            :type do_close: bool
            :param tris: Boolean value.
            :type tris: bool
            :param divs_u: Boolean value.
            :type divs_u: bool
            :param divs_V: Boolean value.
            :type divs_v: bool
            
            ::
            
                my_surf.to_mesh()
            
        """
        
        if not divs_u : divs_u = int(math.ceil(self.domain_u.delta/self.tol_u))
        if not divs_v : divs_v = int(math.ceil(self.domain_v.delta/self.tol_v))
        u_vals = self.domain_u.divide((divs_u),True)
        v_vals = self.domain_v.divide((divs_v),True)

        pts = [self._func(u,v) for v in v_vals for u in u_vals]
        '''
        equiv to
        for v in v_vals:
            for u in u_vals:
                pts.append(self._func(u,v))
        '''
        msh = Mesh(pts)

        res_u = len(u_vals)
        if tris is False:
            # simple quadrangulation style
            for v in range(len(v_vals)):
                row = v*res_u
                for u in range(len(u_vals)-1):
                    pi_0 = row+u
                    pi_1 = row+u+1
                    pi_2 = row+u+res_u+1
                    pi_3 = row+u+res_u
                    msh.add_face(pi_0,pi_1,pi_2,pi_3)
                if do_close:
                    #last two faces in the row
                    pi_0 = row+res_u-1
                    pi_1 = row+0
                    pi_2 = row+res_u
                    pi_3 = row+res_u-1+res_u
                    msh.add_face(pi_0,pi_1,pi_2,pi_3)
        
        else:
            # simple triangulation style
            for v in range(len(v_vals)):
                row = v*res_u
                for u in range(len(u_vals)-1):
                    pi_0 = row+u
                    pi_1 = row+u+1
                    pi_2 = row+u+res_u+1
                    pi_3 = row+u+res_u
                    msh.add_face(pi_0,pi_1,pi_2)
                    msh.add_face(pi_0,pi_2,pi_3)
                if do_close:
                    #last two faces in the row
                    pi_0 = row+res_u-1
                    pi_1 = row+0
                    pi_2 = row+res_u
                    pi_3 = row+res_u-1+res_u
                    msh.add_face(pi_0,pi_1,pi_2)
                    msh.add_face(pi_0,pi_2,pi_3)
        
        return msh

    def isocurve(self, u_val=None, v_val=None):
        """ Returns an isocurve of this Surface at the given u OR v value.
        
            :param u_val: U-value to extract isocurve at.
            :type u_val: float or None
            :param v_val: V-value to extract the isocurve at.
            :type v_val: float or None
            :result: Isocurve of Surface.
            :rtype: Curve
            
            ::
            
                my_surf.isopolyline(u_val=3.5)
                
                OR
                
                my_surf.isopolyline(u_val=None, v_val=2.5)
            
        """
    
        if u_val is None and v_val is None: raise AttributeError("Surface.isocurve requires either u_val OR v_val to be set")
        if u_val is not None and v_val is not None: raise AttributeError("u_val AND v_val cannot both be set when generating a Surface.isocurve")

        if v_val is None:
            # we're plotting a u-iso
            if u_val<self.u0 or u_val>self.u1 : raise DomainError("Isocurve cannot be generated outside the bounds of this Surface's u-domain (%s) %s"%(u_val,self.domain_u))
            def iso_func(t):  return Point(self.func(u_val,t))
            return Curve(iso_func,self.domain_u,self.tol_u)
        else :
            # we're plotting a v-iso
            if v_val<self.v0 or v_val>self.v1 : raise DomainError("Isocurve cannot be generated outside the bounds of this Surface's v-domain (%s) %s"%(v_val,self.domain_v))
            def iso_func(t): return Point(self.func(t,v_val))
            return Curve(iso_func,self.domain_v,self.tol_v)

    def isopolyline(self, u_val = None, v_val = None, dom = None, res = None ):
        """Returns Polyline isocurve of this Surface at the given u OR v value.
        
            :param u_val: U-value to evaluate isocurve at.
            :type u_val: float or None
            :param v_val: V-value to evaluate isocurve at.
            :type v_val: float or None
            :param dom: u or v domain of this Surface. 
            :type dom: Interval or None
            :param res: Resolution of surface.
            :type res: float or None.
            :result: Isocurve of this surface.
            :rtype: Polyline
            
            
        """
        
        if u_val is None and v_val is None: raise AttributeError("Surface.isocurve requires either u_val OR v_val to be set")
        if u_val is not None and v_val is not None: raise AttributeError("u_val AND v_val cannot both be set when generating a Surface.isocurve")

        if v_val is None:
            # we're plotting a u-iso
            if u_val<self.u0 or u_val>self.u1 : raise DomainError("Isocurve cannot be generated outside the bounds of this Surface's u-domain (%s) %s"%(u_val,self.domain_u))
            if dom is None : dom = self.domain_v
            if res is None : res = int(dom.delta / self.tol_v)
            return PLine([self.deval(u_val,v) for v in dom.divide(res,True)])
        else :
            # we're plotting a v-iso
            if v_val<self.v0 or v_val>self.v1 : raise DomainError("Isocurve cannot be generated outside the bounds of this Surface's v-domain (%s) %s"%(v_val,self.domain_v))
            if dom is None : dom = self.domain_u
            if res is None : res = int(dom.delta / self.tol_u)
            return PLine([self.deval(u,v_val) for u in dom.divide(res,True)])


