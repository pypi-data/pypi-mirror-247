import math
from scipy.constants import physical_constants as pyc

none_type = type(None)

epsilon_0 = pyc['vacuum electric permittivity'][0]
K = 1/4/math.pi/epsilon_0


def magnitude(array):

    return math.sqrt(sum([x**2 for x in array]))

def distance(array_u, array_v):

    if len(array_u) != len(array_v):
        raise ValueError('Lengths of arrays mismatch')

    # to use expression with sympy you must not use math.sqrt
    return sum([(u-v)**2 for u, v in zip(array_u, array_v)])**0.5

def inner_product(array_u, array_v):

    if len(array_u) != len(array_v):
        raise ValueError('Lengths of arrays mismatch')

    return sum([u*v for u, v in zip(array_u, array_v)])

def angle(array_u, array_v):

    if len(array_u) != len(array_v):
        raise ValueError('Lengths of arrays mismatch')
    
    return math.acos(inner_product(array_u, array_v)/magnitude(array_u)/magnitude(array_v))

def angle_with_horizontal_2d(point_a, point_b):

    # alpha is the angle between the horizontal axis and the vector formed by point_a and point_b
    # it is positive 0.0 <= alpha <= pi for the first and second quadrants
    # and it is negative -pi <= alpha <= 0.0 for the third and forth quadrants

    if len(point_a) != 2 or len(point_b) != 2:
        raise ValueError('Lengths of arguments \'point_a\' and \'point_b\' must be 2')

    point_c = tuple([b-a for a, b in zip(point_a, point_b)])
    alpha = math.atan2(point_c[1], point_c[0])

    return alpha

def angle_with_horizontal_3d(point_a, point_b):

    # alpha is the angle between the horizontal axis and the projection of the vector formed by point_a and point_b over the x,y plane
    # beta is the angle between the x,y plane and the vector formed by point_a and point_b
    # alpha and beta are positive 0.0 <= alpha <= pi for the first and second quadrants
    # and they are negative -pi <= alpha <= 0.0 for the third and forth quadrants
    # length_xy is the length of the projection of the vector formed by point_a and point_b over the x,y plane

    if len(point_a) != 3 or len(point_b) != 3:
        raise ValueError('Lengths of arguments \'point_a\' and \'point_b\' must be 3')

    point_c = tuple([b-a for a, b in zip(point_a, point_b)])
    length_xy = math.sqrt(point_c[0]**2 + point_c[1]**2)
    alpha = math.atan2(point_c[1], point_c[0])
    beta = math.atan2(point_c[2], length_xy)

    return alpha, beta

def compare_floats(float_ref, float_test, decimals=2):
    
    if not hasattr(float_ref, '__float__') or not hasattr(float_test, '__float__'):
        raise ValueError('Arguments \'float_ref\' and \'float_test\' must be convertible to floats')

    power = round(math.log10(abs(float_ref))) if float_ref != 0.0 else 0.0
    power = power - decimals
    eps = 10**(power)

    return True if float_test - eps <= float_ref <= float_test + eps else False
