import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.vector import Vector

tup = Vector('a', dimensions=3)

def test_item():

    assert len(tup) == 3
    assert tup[0].name == 'a_x'
    assert tup[1].name == 'a_y'
    assert tup[2].name == 'a_z'

def test_iter():

    for value in tup:
        assert value.name in ['a_x', 'a_y', 'a_z']

def test_call():

    tup.define((1, 2, 3))
    assert tup() == (1, 2, 3)

def test_define():

    tup.define([1, 2, 3])
    assert tup[2] == 3

    tup.define(99, 'z')
    assert tup[2] == 99

def test_undefine():

    tup.define((1, 2, 3))

    tup.undefine('z')
    assert hasattr(tup[2], 'name')

    tup.undefine()

    for value in tup:
        assert hasattr(value, 'name')
