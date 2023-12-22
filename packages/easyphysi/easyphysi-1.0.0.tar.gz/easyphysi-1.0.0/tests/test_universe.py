import os
import sys
from contextlib import redirect_stdout

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.universe import Universe


def test_universe_2d():

    g = (0.0, -9.81)
    t = 0.0

    universe = Universe()

    universe.set('g', g)
    universe.set('t', t)

def test_universe_3d():

    g = (0.0, 0.0, -9.81)
    t = 0.0

    universe = Universe(dimensions=3)

    universe.set('g', g)
    universe.set('t', t)

def test_universe_help():

    file = r'tests/ref/universe.txt'

    if os.path.exists(file):
        os.remove(file)

    with open(file, 'w') as f:
        with redirect_stdout(f):
    
            universe = Universe()
            universe.help()

    assert os.path.exists(file)