import math


EPSILON = 1.e-8    # a teeny number, because floating point is inexact
PI = math.pi
TWO_PI = 2 * math.pi


def nearly_zero(x):
    return abs(x) < EPSILON


class Vector:
    """
    >>> isinstance(Vector, object)
    True
    """
    def __init__(self, x, y):
        """
        >>> v = Vector(1, 2)
        >>> v.x, v.y
        (1, 2)
        """
        self.x, self.y = x, y

    def dot(self, other):
        """
        >>> Vector(2, 3).dot(Vector(5, 7))
        31
        """
        return self.x * other.x + self.y * other.y

    def scale(self, other):
        """
        >>> Vector(2, 3).scale(4)
        (8,12)
        """
        return Vector(other * self.x, other * self.y)

    def cross(self, other):
        """
        >>> Vector(2, 3).cross(Vector(5, 7))
        -1
        """
        return self.x * other.y - self.y * other.x

    def __repr__(self):
        """
        >>> Vector(2, 3)
        (2,3)
        """
        return '({0},{1})'.format(self.x, self.y)

    def __add__(self, other):
        """
        >>> Vector(2, 3) + Vector(5, 7)
        (7,10)
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        >>> Vector(2, 3) - Vector(5, 7)
        (-3,-4)
        """
        return self + other.__neg__()

    def __eq__(self, other):
        """
        >>> Vector(2, 3) == Vector(2, 3)
        True
        >>> Vector(2, 3) == Vector(4, 5)
        False
        >>> Vector(2, 3) == Vector(2 + 1.e-10, 3)
        True
        >>> Vector(2, 3) == PI
        Traceback (most recent call last):
            ...
        TypeError: 3.14159265359
        """
        if isinstance(other, Vector):
            return abs(self - other) < EPSILON
        else:
            raise TypeError(other)

    def __neg__(self):
        """
        >>> -Vector(5, 7)
        (-5,-7)
        """
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        """
        >>> Vector(5, 7) * 3
        Traceback (most recent call last):
            ...
        TypeError: 3
        >>> Vector(2, 3) * Vector(5, 7)
        31
        """
        if isinstance(other, Vector):
            return self.dot(other)
        else:
            raise TypeError(other)

    def __rmul__(self, other):
        """
        >>> 3 * Vector(5, 7)
        (15,21)
        >>> 'foo' * Vector(2, 3)
        Traceback (most recent call last):
            ...
        TypeError: foo
        """
        if isinstance(other, int) or isinstance(other, float):
            return Vector(other * self.x, other * self.y)
        else:
            raise TypeError(other)

    def square(self):
        """
        >>> Vector(6, 8).square()
        100
        """
        return self.x * self.x + self.y * self.y

    def __abs__(self):
        """
        >>> abs(Vector(6, 8))
        10.0
        """
        return self.square() ** 0.5

    def normalize(self):
        """
        >>> Vector(6, 8).normalize()
        (0.6,0.8)
        """
        return (1. / abs(self)) * self


class Point(Vector):
    def __add__(self, other):
        assert isinstance(other, Vector) and not isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Point)
        return Vector.__sub__(self, other)


class PSTransform:
    SCALEFACTOR = 72
    ZERO = Point(0, 0)
    ORIGIN = Point(SCALEFACTOR * 4.25, SCALEFACTOR * 5.5)  # center of 8.5x11 sheet of paper
    OFFSET = ORIGIN - ZERO

    def scale(self, distance):
        return self.SCALEFACTOR * distance

    def map(self, xy):
        return self.ORIGIN + self.SCALEFACTOR * (xy - self.ZERO)

    def format(self, str, pt):
        pt = self.map(pt)
        return str.format(pt.x, pt.y)


class LineSegment:
    def __init__(self, point1, point2):
        self.p1, self.p2 = point1, point2

    def postscript(self, tfm):
        """
        >>> tfm = PSTransform()
        >>> LineSegment(Point(0, 0), Point(1, 0)).postscript(tfm)
        '306.0 396.0 lineto 378.0 396.0 moveto'
        """
        return (tfm.format('{0} {1} lineto ', self.p1) +
                tfm.format('{0} {1} moveto', self.p2))

    def __repr__(self):
        """
        >>> LineSegment(Point(0, 0), Point(1, 0))
        LineSegment((0,0), (1,0))
        """
        return 'LineSegment({0}, {1})'.format(self.p1, self.p2)

    def param_to_point(self, param):
        """
        >>> p1, p2 = Point(0, 0), Point(1, 0)
        >>> seg = LineSegment(p1, p2)
        >>> seg.param_to_point(0) == p1
        True
        >>> seg.param_to_point(1) == p2
        True
        >>> seg.param_to_point(0.5) == Point(0.5, 0)
        True
        """
        return self.p1 + param * (self.p2 - self.p1)

    def point_to_param(self, pt):
        """
        >>> seg = LineSegment(Point(0, 0), Point(1, 0))
        >>> seg.point_to_param(Point(0, 1))
        0
        >>> seg.point_to_param(Point(1, 1))
        1
        """
        r = self.p2 - self.p1
        return (pt - self.p1).dot(r) / r.square()

    def parallel(self, other):
        """
        >>> seg = LineSegment(Point(0, 0), Point(1, 0))
        >>> seg.parallel(LineSegment(Point(0, 1), Point(1, 1)))
        True
        >>> seg.parallel(LineSegment(Point(0, 1), Point(1, 2)))
        False
        """
        x, y = self.p2 - self.p1, other.p2 - other.p1
        return nearly_zero(abs(x.cross(y)) / (abs(x) * abs(y)))

    def colinear(self, other):
        """
        >>> seg = LineSegment(Point(0, 0), Point(1, 0))
        >>> seg.colinear(LineSegment(Point(2, 0), Point(3, 0)))
        True
        >>> seg.colinear(LineSegment(Point(0, 1), Point(1, 1)))
        False
        >>> seg.colinear(LineSegment(Point(0, 1), Point(1, 2)))
        False
        """
        p = other.p1
        return self.parallel(other) and p == self.param_to_point(self.point_to_param(p))

    def intersect(self, other):
        """
        See NOTES.md for rationale
        >>> LineSegment(Point(-5,3), Point(5,3)).intersect(LineSegment(Point(-3,-1), Point(-3,5)))
        (-3.0,3.0)
        >>> LineSegment(Point(-5,3), Point(5,3)).intersect(LineSegment(Point(3,3), Point(7,3)))
        LineSegment((3.0,3.0), (5.0,3.0))
        >>> LineSegment(Point(-5,3), Point(5,3)).intersect(LineSegment(Point(3,3), Point(-3,3)))
        LineSegment((-3.0,3.0), (3.0,3.0))
        >>> LineSegment(Point(1,0), Point(2,0)).intersect(LineSegment(Point(0,1), Point(0,2))) is None
        True
        >>> LineSegment(Point(1,0), Point(2,0)).intersect(LineSegment(Point(1,1), Point(2,1))) is None
        True
        >>> LineSegment(Point(1,0), Point(1,2)).intersect(Arc.from_endpoints(Point(0,0), Point(2,0), 1))
        (1.0,1.0)
        >>> LineSegment(Point(1,0), Point(1,2)).intersect(Arc.from_endpoints(Point(0,0), Point(2,0), -1))
        >>> LineSegment(Point(1,0), Point(2,0)).intersect('foo')
        Traceback (most recent call last):
            ...
        TypeError: foo
        """
        if isinstance(other, Arc):
            return other.intersect(self)
        elif not isinstance(other, LineSegment):
            raise TypeError(other)
        S = (self.p2 - self.p1).scale(1.)
        T = (other.p2 - other.p1).scale(1.)
        denom = S.y * T.x - S.x * T.y
        if nearly_zero(denom):
            if nearly_zero(S.cross(other.p1 - self.p1)):
                q1 = (other.p1 - self.p1) * S / (S * S)
                q2 = (other.p2 - self.p1) * S / (S * S)
                if q2 < q1:
                    q1, q2 = q2, q1
                left, right = max(0, q1), min(1, q2)
                if left < right:
                    return LineSegment(self.p1 + left * S, self.p1 + right * S)
            return None
        a = (T.x * (other.p1.y - self.p1.y) - T.y * (other.p1.x - self.p1.x)) / denom
        b = (S.x * (other.p1.y - self.p1.y) - S.y * (other.p1.x - self.p1.x)) / denom
        if 0 <= a <= 1 and 0 <= b <= 1:
            return self.p1 + a * S
        # else return None because we don't intersect


def normalize(angle, a, b):
    while angle < a:
        angle += TWO_PI
    while angle > b:
        angle -= TWO_PI
    return angle


class AngleRange:
    def __init__(self, start, finish):
        # start < finish means we are going CCW
        # start > finish means we are going CW
        # span from start to finish should not exceed TWO_PI
        self.start, self.finish = start, normalize(finish, start - TWO_PI, start + TWO_PI)

    def __repr__(self):
        """
        >>> AngleRange(0, PI)
        <AngleRange 0.0 180.0>
        """
        k = 180. / PI
        return '<AngleRange {0} {1}>'.format(k * self.start, k * self.finish)

    def clockwise(self):
        return self.start < self.finish

    def __contains__(self, angle):
        """
        Here is a clockwise half circle starting from the right side, sweeping up and
        coming back down the left side. It should exclude a point at the bottom and include
        a point at the top.
        >>> r = AngleRange(0, PI)
        >>> (PI / 2) in r
        True
        >>> (3 * PI / 2) in r
        False

        Here is a clockwise half circle starting from the right side, sweeping down and
        coming back up the left side. It should include a point at the bottom and exclude
        a point at the top.
        >>> r = AngleRange(0, -PI)
        >>> (PI / 2) in r
        False
        >>> (3 * PI / 2) in r
        True

        Here is a clockwise half circle starting from the left side, sweeping up and
        coming back down the right side. It should exclude a point at the bottom and include
        a point at the top.
        >>> r = AngleRange(PI, 0)
        >>> (PI / 2) in r
        True
        >>> (3 * PI / 2) in r
        False
        """
        angle = normalize(angle, min(self.start, self.finish), max(self.start, self.finish))
        return (self.start <= angle < self.finish) or (self.finish <= angle < self.start)

    def intersection(self, other):
        """
        >>> AngleRange(0, 1).intersection(AngleRange(2, 3))
        """
        a, b = min(self.start, self.finish), max(self.start, self.finish)
        c, d = min(other.start, other.finish), max(other.start, other.finish)
        a1 = normalize(a, 0, TWO_PI)
        a, b = a1, b + a1 - a
        c1 = normalize(c, 0, TWO_PI)
        c, d = c1, d + c1 - c
        e, f = max(a, c), min(b, d)
        if f >= e:
            return AngleRange(e, f)
        else:
            return None  # no overlap


class Arc:
    def __init__(self, center, radius, start_angle, end_angle):
        # angles are in radians, we convert to degrees for Postscript
        assert radius >= 0
        self.center, self.radius, self.angle_range = center, radius, AngleRange(start_angle, end_angle)

    def postscript(self, tfm):
        """
        >>> tfm, center = PSTransform(), Point(1, 0)

        upper half circle
        >>> Arc(center, 1, PI, 0).postscript(tfm)
        '378.0 396.0 72 0.0 180.0 arc'
        >>> Arc(center, 1, 0, PI).postscript(tfm)
        '378.0 396.0 72 0.0 180.0 arc'

        lower half circle
        >>> Arc(center, 1, PI, TWO_PI).postscript(tfm)
        '378.0 396.0 72 180.0 360.0 arc'
        >>> Arc(center, 1, TWO_PI, PI).postscript(tfm)
        '378.0 396.0 72 180.0 360.0 arc'

        %!PS-Adobe-2.0
        378.0 396.0 72 180.0 0.0 arcn
        stroke showpage
        """
        k = 180. / PI
        if self.angle_range.clockwise():
            a, b = self.angle_range.start, self.angle_range.finish
        else:
            a, b = self.angle_range.finish, self.angle_range.start
        return (tfm.format('{0} {1} ', self.center) +
                '{0} '.format(tfm.scale(abs(self.radius))) +
                '{0} {1} '.format(k * a, k * b) + 'arc')

    @classmethod
    def from_endpoints(cls, p1, p2, radius):
        """
        >>> p1, p2 = Point(0, 0), Point(2, 0)
        >>> Arc.from_endpoints(p1, p2, 1)
        Arc((1.0,0.0),1,180.0,0.0)
        >>> Arc.from_endpoints(p1, p2, -1)
        Arc((1.0,0.0),1,180.0,360.0)
        >>> Arc.from_endpoints(p2, p1, 1)
        Arc((1.0,0.0),1,360.0,180.0)
        >>> Arc.from_endpoints(p2, p1, -1)
        Arc((1.0,0.0),1,0.0,180.0)

        >>> p1, p2, r = Point(1, 1), Point(1, -1), 2**.5
        >>> Arc.from_endpoints(p1, p2, r)
        Arc((-2.22044604925e-16,0.0),1.41421356237,45.0,-45.0)
        >>> Arc.from_endpoints(p2, p1, -r)
        Arc((-2.22044604925e-16,0.0),1.41421356237,-45.0,45.0)

        >>> p1, p2, r = Point(-1, 1), Point(-1, -1), 2**.5
        >>> Arc.from_endpoints(p1, p2, -r)
        Arc((2.22044604925e-16,0.0),1.41421356237,135.0,225.0)
        >>> Arc.from_endpoints(p2, p1, r)
        Arc((2.22044604925e-16,0.0),1.41421356237,225.0,135.0)

        >>> p1, p2 = Point(1, 0), Point(0, 1)
        >>> Arc.from_endpoints(p1, p2, 1).center
        (1.0,1.0)
        >>> Arc.from_endpoints(p2, p1, -1).center
        (1.0,1.0)
        >>> Arc.from_endpoints(p1, p2, -1).center
        (0.0,0.0)
        >>> Arc.from_endpoints(p2, p1, 1).center
        (0.0,0.0)

        >>> Arc.from_endpoints(p1, p2, 0.1)
        Traceback (most recent call last):
            ...
        Exception: radius is too small for this arc, make it bigger
        """
        # radius > 0 means we go clockwise from p1 to p2, radius < 0 means we go counter-clockwise
        x = p2 - p1
        if radius**2 < 0.25 * x.dot(x):
            raise Exception("radius is too small for this arc, make it bigger")
        w = (radius**2 - 0.25 * x.dot(x)) ** .5
        wn = Vector(x.y, -x.x).normalize()
        if radius * wn.cross(x) < 0:
            wn = -wn
        center = p1 + 0.5 * x + w * wn

        def get_angle(p):
            return math.atan2(p.y, p.x)
        a, b = get_angle(p1-center), get_angle(p2-center)
        if radius < 0:
            while b < a:
                b += TWO_PI
        else:
            while a < b:
                a += TWO_PI
        return cls(center, abs(radius), a, b)

    def __repr__(self):
        k = 180. / PI
        start, finish = k * self.angle_range.start, k * self.angle_range.finish
        return 'Arc({0},{1},{2},{3})'.format(self.center, self.radius, start, finish)

    def intersect(self, other):
        """
        >>> me = Arc.from_endpoints(Point(0,0), Point(2,0), 1)
        >>> me.intersect('foo')
        Traceback (most recent call last):
            ...
        TypeError: foo
        >>> me.intersect(LineSegment(Point(1,0), Point(1,2)))
        (1.0,1.0)
        >>> me.intersect(Arc.from_endpoints(Point(1,0), Point(2,0), 1))
        [(2.0,1.11022302463e-16)]
        >>> me.intersect(Arc.from_endpoints(Point(1,0), Point(3,1), 1.5))
        [(1.56951603584,0.821980221736)]

        >>> p0 = Point(0, 0)
        >>> Arc(p0, 1, 0, TWO_PI).intersect(Arc(p0, 2, 0, TWO_PI))
        >>> Arc(p0, 1, 0, PI).intersect(Arc(p0, 1, PI/2, 3*PI/2))
        Arc((0,0),1,90.0,180.0)
        >>> Arc(p0, 1, 0, TWO_PI).intersect(Arc(Point(1, 0), 1, 0, TWO_PI))
        [(0.5,0.866025403784), (0.5,-0.866025403784)]

        >>> Arc(p0, 1, 0, TWO_PI).intersect(LineSegment(Point(2, 1), Point(2, -1)))
        >>> Arc(p0, 1, 0, TWO_PI).intersect(LineSegment(Point(1, 1), Point(1, -1)))
        (1.0,0.0)
        >>> Arc(p0, 1, 0, TWO_PI).intersect(LineSegment(Point(0.5, 1), Point(0.5, -1)))
        [(0.5,-0.866025403784), (0.5,0.866025403784)]
        """
        if isinstance(other, Arc):
            if self.center == other.center:
                if nearly_zero(self.radius - other.radius):
                    v = Arc(self.center, self.radius, 0, 0)
                    v.angle_range = self.angle_range.intersection(other.angle_range)
                    return v
                else:
                    return None
            else:
                # find the two points where the circles intersect
                # filter them by the angle ranges of both arcs, must be in both to survive
                # return list of surviving points, or None
                k = 1. / abs(self.center - other.center)
                theta = math.atan2(other.center.y - self.center.y, other.center.x - self.center.x)
                r1 = k * self.radius
                r2 = k * other.radius
                intersections = []
                # u and v are in a coordinate system that has been scaled, rotated, and translated
                # to move the two centers to (0, 0) and (1, 0) to simplify some of the math.
                u = (r1**2 + 1 - r2**2) / 2
                if abs(r1) >= abs(u):
                    v = (r1**2 - u**2) ** .5
                    # Transform u and v back into the original coordinate system.
                    x1 = self.center.x + (u * math.cos(theta) - v * math.sin(theta)) / k
                    y1 = self.center.y + (v * math.cos(theta) + u * math.sin(theta)) / k
                    p = Point(x1, y1)
                    if self.included_angle(p) and other.included_angle(p):
                        intersections.append(Point(x1, y1))
                    if not nearly_zero(r1 - u):
                        x2 = self.center.x +  (u * math.cos(theta) + v * math.sin(theta)) / k
                        y2 = self.center.y + (-v * math.cos(theta) + u * math.sin(theta)) / k
                        p2 = Point(x2, y2)
                        if self.included_angle(p2) and other.included_angle(p2):
                            intersections.append(p2)
                return intersections or None
        elif isinstance(other, LineSegment):
            c = (self.center - other.p2).square() - self.radius**2
            b = 2 * (other.p1 - other.p2).dot(other.p2 - self.center)
            a = (other.p1 - other.p2).square()
            det = b**2 - 4 * a * c
            if det < 0:
                return None
            elif nearly_zero(det):
                pts = [-b / (2. * a)]
            else:
                pts = [(-b + det**0.5) / (2 * a), (-b - det**0.5) / (2 * a)]
            pts = map(other.param_to_point,
                      filter(lambda root: 0 <= root <= 1, pts))
            pts = filter(self.included_angle, pts)
            if len(pts) == 0:
                return None
            elif len(pts) == 1:
                return pts[0]
            else:
                return pts
        raise TypeError(other)

    def included_angle(self, pt):
        """
        >>> p1, p2, p3, p4 = Point(0, 0), Point(2, 0), Point(1, 1), Point(2, 2)
        >>> Arc.from_endpoints(p1, p2, 1).included_angle(p3)
        True
        >>> Arc.from_endpoints(p1, p2, -1).included_angle(p3)
        False
        >>> Arc.from_endpoints(p2, p1, 1).included_angle(p3)
        False
        >>> Arc.from_endpoints(p2, p1, -1).included_angle(p3)
        True
        >>> p1, p2, p3 = Point(1, 0), Point(0, 1), Point(1, 1)
        >>> Arc.from_endpoints(p1, p2, -1).included_angle(p3)
        True
        >>> Arc.from_endpoints(p2, p1, 1).included_angle(p3)
        True
        >>> Arc.from_endpoints(p1, p2, 1).included_angle(p4)
        False
        >>> Arc.from_endpoints(p2, p1, -1).included_angle(p4)
        False
        """
        r = pt - self.center
        return math.atan2(r.y, r.x) in self.angle_range


class Shape:
    def __init__(self, points, radii=None):
        self.segments = []
        n = len(points)
        if radii is None:
            radii = n * [None]
        for i in range(n):
            p1, p2 = points[i], points[(i+1) % n]
            if radii[i] is None:
                self.segments.append(LineSegment(p1, p2))
            else:
                self.segments.append(Arc.from_endpoints(p1, p2, radii[i]))

    def postscript(self, tfm):
        middle = ' '.join([segment.postscript(tfm) for segment in self.segments])
        return '{0} stroke'.format(middle)


############

def rectangle(xcenter, ycenter, width, height):
    """
    >>> rectangle(0, 0, 5, 3).segments
    [LineSegment((-5,-3), (-5,3)), LineSegment((-5,3), (5,3)), LineSegment((5,3), (5,-3)), LineSegment((5,-3), (-5,-3))]
    """
    x1, x2 = xcenter - width, xcenter + width
    y1, y2 = ycenter - height, ycenter + height
    return Shape([Point(x1, y1), Point(x1, y2), Point(x2, y2), Point(x2, y1)])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
