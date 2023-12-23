import sys
from sympy import Symbol

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.utils import compare_floats, magnitude, distance, inner_product, angle, angle_with_horizontal_2d, angle_with_horizontal_3d


def test_compare_floats_small():

    assert compare_floats(1, 1.01)
    assert not compare_floats(1, 1.011)
    assert not compare_floats(1, 0.981)
    assert compare_floats(3.14, 3.1416)
    assert compare_floats(3.14E-10, 3.1416E-10)
    assert compare_floats(3.14E-10, 3.15E-10)
    assert not compare_floats(3.14E-10, 3.151E-10)

def test_compare_floats_big():

    assert compare_floats(1E+2, 1.01E+2)
    assert not compare_floats(1E+2, 1.011E+2)
    assert not compare_floats(1E+2, 0.981E+2)
    assert compare_floats(3.14E+2, 3.1416E+2)
    assert compare_floats(3.14E+10, 3.1416E+10)
    assert compare_floats(3.14E+10, 3.15E+10)
    assert not compare_floats(3.14E+10, 3.151E+10)

def test_magnitude():

    u = (3, 4)
    assert magnitude(u) == 5.0

    v = (3.1416, 4.1234)
    assert compare_floats(magnitude(v), 5.18383, decimals=4)

def test_distance():

    u = (223.2, 34)
    v = (45, 3.1)

    assert compare_floats(distance(u, v), 180.8592, decimals=4)

def test_inner_product():

    u = (2, -3)
    v = (5, 1)

    assert compare_floats(inner_product(u, v), 7)

def test_angle():

    u = (2, 1, -2)
    v = (1, 1, 1)

    assert compare_floats(angle(u, v), 1.37)

def test_angle_with_horizontal_2d():

    p0 = (0, 0)
    p1 = (5, 5)
    p2 = (-5, 5)
    p3 = (-5, -5)
    p4 = (5, -5)

    assert compare_floats(angle_with_horizontal_2d(p0, p1), +0.79)
    assert compare_floats(angle_with_horizontal_2d(p0, p2), +2.36)
    assert compare_floats(angle_with_horizontal_2d(p0, p3), -2.36)
    assert compare_floats(angle_with_horizontal_2d(p0, p4), -0.79)
    assert compare_floats(angle_with_horizontal_2d(p1, p0), -2.36)
    assert compare_floats(angle_with_horizontal_2d(p2, p0), -0.79)
    assert compare_floats(angle_with_horizontal_2d(p3, p0), +0.79)
    assert compare_floats(angle_with_horizontal_2d(p4, p0), +2.36)
    assert compare_floats(angle_with_horizontal_2d(p1, p2), +3.14)
    assert compare_floats(angle_with_horizontal_2d(p2, p3), -1.57)
    assert compare_floats(angle_with_horizontal_2d(p3, p4), 0.0)
    assert compare_floats(angle_with_horizontal_2d(p4, p1), +1.57)

    pa = (0, -3)
    pb = (4, 0)

    assert compare_floats(angle_with_horizontal_2d(pa, pb), 0.64)

def test_angle_with_horizontal_3d():

    pa = (0, -3, 0)
    pb = (4, 0, 5)

    alpha, beta = angle_with_horizontal_3d(pa, pb)

    assert compare_floats(alpha, 0.64)
    assert compare_floats(beta, 0.79)
