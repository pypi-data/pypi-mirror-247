
import sys
import math
from sympy import Symbol

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.body import Body
from easyphysi.drivers.universe import Universe
from easyphysi.drivers.system import System
from easyphysi.utils import compare_floats, magnitude


def test_newton_14():
    """
    URL: https://fq.iespm.es/documentos/rafael_artacho/4_ESO/08.%20Problemas%20Las%20fuerzas.pdf
    Problem: 14
    Statement: The following ramp has an inclination of 25º. Determine the force that must be exerted on the 250 kg wagon to make it go up with constant velocity:
    a) If there is no friction.
    b) If 𝜇 = 0.1.
    """
    mu = Symbol('mu')
    alpha = math.radians(25)
    m = 250
    g = 9.81
    W = (-m*g*math.sin(alpha), -m*g*math.cos(alpha))
    N = (0.0, m*g*math.sin(alpha))
    Fr = (-mu*m*g*math.cos(alpha), 0.0)

    body = Body('body')

    body.set('m', m)
    body.add_force('W', W)
    body.add_force('Fr', Fr)
    body.add_force('N', N)

    universe = Universe()
    universe.add_body(body)

    a_x, a_y = universe.newton_equation('body').solve(['a_x', 'a_y'])
    f_00 = m*a_x[0].subs('mu', 0.0)
    f_01 = m*a_x[0].subs('mu', 0.1)

    assert compare_floats(f_00, -1036.47)
    assert compare_floats(f_01, -1258.74)

def test_newton_14b_bis():
    """
    URL: https://fq.iespm.es/documentos/rafael_artacho/4_ESO/08.%20Problemas%20Las%20fuerzas.pdf
    Problem: 14b
    Statement: The following ramp has an inclination of 25º. Determine the force that must be exerted on the 250 kg wagon to make it go up with constant velocity:
    b) If 𝜇 = 0.1.
    """
    mu = 0.1
    alpha = math.radians(25)
    m = 250
    g = 9.81
    W = (-m*g*math.sin(alpha), -m*g*math.cos(alpha))
    N = (0.0, m*g*math.sin(alpha))
    Fr = (-mu*m*g*math.cos(alpha), 0.0)

    body = Body('body')

    body.set('m', m)
    body.add_force('W', W)
    body.add_force('Fr', Fr)
    body.add_force('N', N)

    universe = Universe()
    universe.add_body(body)

    a_x, a_y = universe.newton_equation('body').solve(['a_x', 'a_y'])
    f_x = m*a_x[0]

    assert compare_floats(a_x[0], -5.03)
    assert compare_floats(a_y[0], -4.74)
    assert compare_floats(f_x, -1258.74)

def test_newton_14b_bis_bis():

    mu = 0.1
    sin_alpha = Symbol('sin_alpha')
    cos_alpha = Symbol('cos_alpha')
    m = 250
    g = 9.81
    a = (-5.03497308675920, -4.74499424315328)
    W = (-m*g*sin_alpha, -m*g*cos_alpha)
    N = (0.0, m*g*sin_alpha)
    Fr = (-mu*m*g*cos_alpha, 0.0)

    body = Body('body')

    body.set('m', m)
    body.set('a', a)
    body.add_force('W', W)
    body.add_force('Fr', Fr)
    body.add_force('N', N)

    universe = Universe()
    universe.add_body(body)

    sin_alpha, cos_alpha = universe.newton_equation('body').solve(['sin_alpha', 'cos_alpha'])

    assert compare_floats(math.degrees(math.asin(sin_alpha[0])), 25)
    assert compare_floats(math.degrees(math.acos(cos_alpha[0])), 25)

def test_newton_8():
    """
    File: Examen cinemática y dinámica
    Problem: 8
    Statement: In the system shown in the figure, the three masses are mA = 1 kg, mB = 2 kg, and mC = 1.5 kg. If the coefficient of friction is 𝜇 = 0.223, calculate the acceleration of the system when it is released.
    """
    # initialize parameters and constants
    g = 9.81
    mu = 0.223
    alpha = math.radians(30)
    ma, mb, mc = 1, 2, 1.5

    # define known forces
    Fra = (-mu*ma*g*math.cos(alpha), 0.0)
    Frb = (-mu*mb*g, 0.0)
    Wa = (-ma*g*math.sin(alpha), -ma*g*math.cos(alpha))
    Wc = (mc*g, 0.0)

    # define unknown forces
    Tab = (Symbol('T2'), 0.0)
    Tba = (-Symbol('T2'), 0.0)
    Tbc = (Symbol('T1'), 0.0)
    Tcb = (-Symbol('T1'), 0.0)
    
    # define bodies and apply forces
    body_a = Body('A')
    body_a.set('m', ma)
    body_a.add_force('T2', Tab)
    body_a.add_force('Fra', Fra)
    body_a.add_force('Wa', Wa)

    body_b = Body('B')
    body_b.set('m', mb)
    body_b.add_force('T1', Tbc)
    body_b.add_force('T2', Tba)
    body_b.add_force('Frb', Frb)

    body_c = Body('C')
    body_c.set('m', mc)
    body_c.add_force('Wc', Wc)
    body_c.add_force('T1', Tcb)

    universe = Universe()
    universe.add_body(body_a)
    universe.add_body(body_b)
    universe.add_body(body_c)

    # Get newton equation for each body

    eq_a = universe.newton_equation('A')['x']
    eq_b = universe.newton_equation('B')['x']
    eq_c = universe.newton_equation('C')['x']

    # Then solve system:

    unknowns = ['T1', 'T2', 'a_x']

    system = System()
    system.add_equation(eq_a)
    system.add_equation(eq_b)
    system.add_equation(eq_c)
    
    T1, T2, a_x = system.solve(unknowns)
    
    assert compare_floats(T1[0], 13.54)
    assert compare_floats(T2[0], 7.59)
    assert compare_floats(a_x[0], 0.79)

def test_newton_8_bis():
    """
    File: Examen cinemática y dinámica
    Problem: 8
    Statement: In the system shown in the figure, the three masses are mA = 1 kg, mB = 2 kg, and mC = 1.5 kg. If the coefficient of friction is 𝜇 = 0.223, calculate the acceleration of the system when it is released.
    """
    # initialize parameters and constants
    g = 9.81
    mu = 0.223
    alpha = math.radians(30)
    ma = 1
    mb = 2
    mc = 1.5

    # define known forces
    Fra = (-mu*ma*g*math.cos(alpha), 0.0)
    Frb = (-mu*mb*g, 0.0)
    Wa = (-ma*g*math.sin(alpha), -ma*g*math.cos(alpha))
    Wc = (mc*g, 0.0)

    # define unknown forces
    Tab = (Symbol('T2'), 0.0)
    Tba = (-Symbol('T2'), 0.0)
    Tbc = (Symbol('T1'), 0.0)
    Tcb = (-Symbol('T1'), 0.0)
    
    # define bodies and apply forces
    body = Body('body')
    body.set('m', ma+mb+mc)
    body.add_force('T2', Tab)
    body.add_force('Fra', Fra)
    body.add_force('Wa', Wa)
    body.add_force('T1', Tbc)
    body.add_force('T2', Tba)
    body.add_force('Frb', Frb)
    body.add_force('Wc', Wc)
    body.add_force('T1', Tcb)

    universe = Universe()
    universe.add_body(body)

    # Solve for a
    a_x, a_y = universe.newton_equation('body').solve(['a_x', 'a_y'])
    a = magnitude((a_x[0], a_y[0]))
    
    assert compare_floats(a_x[0], 0.79)
    assert compare_floats(a_y[0], -1.89)
    assert compare_floats(a, 2.05)
