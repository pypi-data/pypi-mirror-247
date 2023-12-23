
import os
import sys
import math
from sympy import Symbol

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.body import Body
from easyphysi.drivers.universe import Universe


def test_plot_scalar_equation():
    """
    """
    file = './tests/ref/vf_f_v0.png'

    m = 1.0
    v0 = Symbol('v0')
    alpha = math.radians(30)
    length = 2.0
    g = 9.81
    h0 = length*math.sin(alpha)
    hf = 0.0
    vf = Symbol('vf')

    Ep0 = m*g*h0
    Ek0 = 1/2*m*v0**2
    Epf = -m*g*hf
    Ekf = -1/2*m*vf**2

    body = Body('body')

    body.add_energy('Ep0', Ep0)
    body.add_energy('Ek0', Ek0)
    body.add_energy('Epf', Epf)
    body.add_energy('Ekf', Ekf)

    universe = Universe()
    universe.add_body(body)

    if os.path.exists(file):
        os.remove(file)

    universe.energy_conservation_equation('body').plot('vf', 'v0', [0, 4], points=200, path=file, show=False)

    assert os.path.exists(file)