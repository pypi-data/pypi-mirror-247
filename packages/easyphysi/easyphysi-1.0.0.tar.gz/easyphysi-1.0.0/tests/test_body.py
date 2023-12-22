import os
import sys
from contextlib import redirect_stdout

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.body import Body


def test_body_2d():

    a = (0.0, -9.81)
    p = (0.0, 1.0)

    body = Body('A')

    body.set('a', a)
    body.set('p_x', p[0])
    body.set('p_y', p[1])

def test_body_3d():

    a = (0.0, 0.0, -9.81)
    p = (0.0, 1.0, 2.0)

    body = Body('A', dimensions=3)

    body.set('a', a)
    body.set('p_x', p[0])
    body.set('p_y', p[1])
    body.set('p_z', p[2])

def test_body_help():

    file = r'tests/ref/body.txt'

    if os.path.exists(file):
        os.remove(file)

    with open(file, 'w') as f:
        with redirect_stdout(f):
    
            body = Body('A')
            body.help()

    assert os.path.exists(file)
