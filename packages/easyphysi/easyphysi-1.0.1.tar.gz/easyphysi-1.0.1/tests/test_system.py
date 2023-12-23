import os
import sys
import math
from sympy import Symbol

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.utils import compare_floats
from easyphysi.drivers.equation import Equation
from easyphysi.drivers.system import System
from easyphysi.drivers.body import Body
from easyphysi.drivers.universe import Universe


def test_system():

    n = Symbol('n')
    y1 = Symbol('y1')
    y2 = Symbol('y2')

    equation_0 = Equation(165*y1 - 0.310*n - 0.517*n)
    equation_1 = Equation(165*y2 - 0.173*n - 0.517*n)
    equation_2 = Equation(y1 + y2 - 1.0)

    system = System()
    system.add_equation(equation_0)
    system.add_equation(equation_1)
    system.add_equation(equation_2)

    unknowns = ['n', 'y1', 'y2']

    n, y1, y2 = system.solve(unknowns)

    assert compare_floats(n[0], 108.77)
    assert compare_floats(y1[0], 0.55)
    assert compare_floats(y2[0], 0.45)

def test_plot_system():
    """
    F2-PAU-Gravitation
    B1.a 2019 junio
    """
    
    file = './tests/ref/F_f_ma.png'
    ma = Symbol('ma')

    body_a = Body('A')
    body_a.set('m', ma)
    body_a.set('p', (0, 0))

    body_b = Body('B')
    body_b.set('m', 5)
    body_b.set('p', (2, -2))

    universe = Universe()
    universe.add_body(body_a)
    universe.add_body(body_b)

    if os.path.exists(file):
        os.remove(file)

    universe.gravitational_force_equation('B').plot(['Fg_x', 'Fg_y'], 'ma', [0, 5], points=200, path=file, show=False)

    assert os.path.exists(file)