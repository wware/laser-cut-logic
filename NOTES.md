Stuff about how to approach this
==

As much as possible, do things in a Postscript-like style to keep Postscript generation simple.

* A circular curve can compute Postscript parameters: center, radius, start and end angles.
* A segment is either a circular curve or a line segment, connecting two points.
* A path is a sequences of points connected by line segments or circular curves.
* A shape is a path whose first and last points are the same, and it doesn't cross itself.
* Operations on shapes include union, intersection, and difference.

How do you make sure a shape doesn't cross itself? That is an N-squared computation on the segments.
Sequential segments should intersect only at their endpoints, and only in sequence. There will be
lots of shapes that don't need to be checked for this: rectangles, triangles, circles, etc.

How do you determine if a point lies inside a shape?
```python
ON_BOUNDARY = object()

if the point lies on any segment of the shape:
    return ON_BOUNDARY
while True:
    r = Ray in random direction, originating at the point
    if r does not intersect any of the points of the shape:
        break
n = 0
for segment in the segments for the shape:
    n += number of intersections of ray with segment
return (n is odd)
```

You draw a ray from the point in a random direction.
If the ray intersects any of the points comprising the shape, choose a new ray. Count the intersections
of the ray with the shape's segments. If that count is odd, the point is inside, if

Functions I'll need:

* Given a point and a segment, return true iff the point is on the line segment
* Given a ray and a segment, return the point(s) of intersection, or None
* Given two segments, return None or point(s) of intersection or a segment representing their intersection

Shapes are specified programmatically and generate Postscript on demand. Usually a shape will be
start out as a basic geometric object (circle, triangle, rectangle, etc.) and it will be modified
by chaining method calls that each return a new shape.

Combining shapes via union
--

A shape can be considered a cyclic graph of vertices and edges. When two shapes interact to produce
a union (__add__), intersection (__and__), or difference (__sub__), we create new vertices where the
shapes cross and merge the two cyclic graphs, then as appropriate we choose a new cyclic subgraph.
We need to be cognizant of where the interiors of the two shapes are. Any vertex will have one of
the following relationships to each shape: inside, outside, or on the perimeter. We use those
relationships to guide our traversal in creating the new cyclic graph.

The exceptional case is where the shapes share an edge (straight or curved) for some non-zero
length. Then we have a combined graph that looks like a figure-8 instead of two interlocked loops.
There will be one or more edges that are common to the two loops, and on the perimeters of both
original shapes. So you need to think about that when doing the traversal.

When two shapes are combined via union, they are either overlapping (e.g. a circle overlapping
with a rectangle) or they share a section of perimeter (e.g. two rectangles have overlapping colinear edges).

First case: find all the perimeter intersections.

Annoying linear algebra
--

I don't want a dependency on numpy to do linear algebra in 2 dimensions. Let's do it explicitly.
Set up some variables. Given two line segments, one connecting points p1 and p2, the other connecting
points q1 and q2, first define difference vectors S and T, then coefficients a and b.
```
    S = p2 - p1, T = q2 - q1
    p1 + a*S = q1 + b*T
    p1x + a*Sx = q1x + b*Tx, p1y + a*Sy = q1y + b*Ty

    [ Sx  -Tx ][ a ]   [ q1x-p1x ]
    [         ][   ] = [         ]
    [ Sy  -Ty ][ b ]   [ q1y-p1y ]

    Inverting the 2x2 matrix gives
         1      [ -Ty  Tx ][ q1x-p1x ]   [ a ]
    ----------- [         ][         ] = [   ]
    SyTx - SyTx [ -Sy  Sx ][ q1y-p1y ]   [ b ]
```

If SyTx = SyTx to within a small tolerance (since we're dealing with floating point numbers), then the
line segments are parallel, and either we have a line segment overlap or we have no intersection at all.
We have an intersection if we can solve for a and b, and if they satisfy 0 <= a,b <= 1.

Assuming they are parallel, how to determine if they're colinear? That would be the case if
```
    S.cross(q1-p1) = 0
```
and again this needs to be done with a tolerance to allow for floating point arithmetic fuzziness.
