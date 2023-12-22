import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/easyphysi')

from easyphysi.drivers.body import Body, electron
from easyphysi.drivers.universe import Universe
from easyphysi.utils import compare_floats, magnitude


def test_electrical_a3a_2021_modelo():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.a 2021 modelo
    Statement: Two equal point charges of 5 nC are located on the (x, y) plane at points (0, 3) m and (0, -3) m.
    a) Determine the electric field created by both charges at the point (4, 0) m.
    """
    point = (4, 0)

    body_1 = Body('1')
    body_1.set('q', 5E-9)
    body_1.set('p', (0, +3))

    body_2 = Body('2')
    body_2.set('q', 5E-9)
    body_2.set('p', (0, -3))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)

    Ee_x, Ee_y = universe.electrical_field_intensity_equation(point).solve(['Ee_x', 'Ee_y'])
    Ee = magnitude((Ee_x[0], Ee_y[0]))

    assert compare_floats(Ee_x[0], 2.88)
    assert compare_floats(Ee_y[0], 0.0)
    assert compare_floats(Ee, 2.88)

def test_electrical_a3b_2021_modelo_bis():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.a 2021 modelo
    Statement: Two equal point charges of 5 nC are located on the (x, y) plane at points (0, 3) m and (0, -3) m.
    """
    point_0 = (0, 0)
    point_1 = (4, 0)

    body_1 = Body('1')
    body_1.set('q', 5E-9)
    body_1.set('p', (0, +3))

    body_2 = Body('2')
    body_2.set('q', 5E-9)
    body_2.set('p', (0, -3))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)

    Ve_0 = universe.electrical_potential_equation(point_0).solve('Ve')
    Ve_1 = universe.electrical_potential_equation(point_1).solve('Ve')

    assert compare_floats(Ve_0[0], 30)
    assert compare_floats(Ve_1[0], 18)

def test_electrical_a3a_2019_junio_coincidentes():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.a 2019 junio coincidentes
    Statement: Two identical particles with a charge Q = -3 nC are fixed at the points (0, 3) and (0, -3) m in the xy-plane.
    a) Determine the electric field created by both charges at the point (4, 0) m.
    """
    point = (4, 0)

    body_1 = Body('1')
    body_1.set('q', -3E-9)
    body_1.set('p', (0, +3))

    body_2 = Body('2')
    body_2.set('q', -3E-9)
    body_2.set('p', (0, -3))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)

    Ee_x, Ee_y = universe.electrical_field_intensity_equation(point).solve(['Ee_x', 'Ee_y'])
    Ee = magnitude((Ee_x[0], Ee_y[0]))

    assert compare_floats(Ee_x[0], -1.73)
    assert compare_floats(Ee_y[0], 0.0)
    assert compare_floats(Ee, 1.73)

def test_electrical_a3a_2019_junio_coincidentes_bis():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.b 2019 junio coincidentes
    Statement: Two identical particles with a charge Q = -3 nC are fixed at the points (0, 3) and (0, -3) m in the xy-plane.
    a) Determine the electric field created by both charges at the point (4, 0) m.
    """
    point_0 = (0, 0)
    point_1 = (4, 0)

    body_1 = Body('1')
    body_1.set('q', -3E-9)
    body_1.set('p', (0, +3))

    body_2 = Body('2')
    body_2.set('q', -3E-9)
    body_2.set('p', (0, -3))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)

    Ve_0 = universe.electrical_potential_equation(point_0).solve('Ve')
    Ve_1 = universe.electrical_potential_equation(point_1).solve('Ve')

    assert compare_floats(Ve_0[0], -18)
    assert compare_floats(Ve_1[0], -10.8)

def test_electrical_a3a_2021_junio_coincidentes_a():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.a 2021 junio coincidentes
    Statement: At the vertices of a square with a side of 2 m and centered at the origin of coordinates, four electric charges are placed as shown in the figure.
    a) Obtain the electric field created by the charges at the center of the square.
    """
    point = (0, 0)

    body_1 = Body('1')
    body_1.set('q', 5E-9)
    body_1.set('p', (-1, +1))

    body_2 = Body('2')
    body_2.set('q', 5E-9)
    body_2.set('p', (+1, +1))

    body_3 = Body('3')
    body_3.set('q', 3E-9)
    body_3.set('p', (+1, -1))

    body_4 = Body('4')
    body_4.set('q', 3E-9)
    body_4.set('p', (-1, -1))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)
    universe.add_body(body_3)
    universe.add_body(body_4)

    Ee_x, Ee_y = universe.electrical_field_intensity_equation(point).solve(['Ee_x', 'Ee_y'])
    Ee = magnitude((Ee_x[0], Ee_y[0]))

    assert compare_floats(0.0, Ee_x[0])
    assert compare_floats(-12.72, Ee_y[0])
    assert compare_floats(12.72, Ee)

def test_electrical_a3b_2021_junio_coincidentes():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.b 2021 junio coincidentes
    Statement: b) If an electron is launched from the center of the square with a velocity v = 3E4 j m/s, calculate the speed at which the electron will leave the square through the midpoint of the top side.
    """
    point_0 = (0, 0)
    point_1 = (0, 1)

    body_1 = Body('1')
    body_1.set('q', 5E-9)
    body_1.set('p', (-1, +1))

    body_2 = Body('2')
    body_2.set('q', 5E-9)
    body_2.set('p', (+1, +1))

    body_3 = Body('3')
    body_3.set('q', 3E-9)
    body_3.set('p', (+1, -1))

    body_4 = Body('4')
    body_4.set('q', 3E-9)
    body_4.set('p', (-1, -1))

    universe = Universe()
    universe.add_body(body_1)
    universe.add_body(body_2)
    universe.add_body(body_3)
    universe.add_body(body_4)
    universe.add_body(electron)

    electron.set('p', point_0)

    Ue_0 = universe.electrical_potential_energy_equation('electron').solve('Ue')

    electron.set('p', point_1)
    
    Ue_1 = universe.electrical_potential_energy_equation('electron').solve('Ue')

    W = Ue_0[0] - Ue_1[0]  # W = -AUe = Ue_0 - Ue_1

    assert compare_floats(1.97E-18, W)

def test_electrical_a3b_2023_modelo():
    """
    URL: https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/content/home/recursos/recursospau/ficherospaufisicaporbloques/F4.1-PAU-CampoEl%C3%A9ctrico.pdf
    Problem: A3.b 2023 modelo
    Statement: A hollow spherical shell with a radius of 3 cm and centered at the origin of coordinates is charged with a uniform surface charge density σ = 2 µC/m2.
    b) Obtain the work done by the electric field to move a particle with a charge of 1 nC from the point (0, 2, 0) m to the point (3, 0, 0) m.
    """
    point_0 = (0, 2, 0)
    point_1 = (3, 0, 0)

    sphere = Body('sphere', dimensions=3)
    sphere.set('q', 22.62E-9)
    sphere.set('p', (0, 0, 0))

    point = Body('point', dimensions=3)
    point.set('q', 1E-9)

    universe = Universe(dimensions=3)
    universe.add_body(sphere)
    universe.add_body(point)

    point.set('p', point_0)

    Ue_0 = universe.electrical_potential_energy_equation('point').solve('Ue')

    point.set('p', point_1)
    
    Ue_1 = universe.electrical_potential_energy_equation('point').solve('Ue')

    W = Ue_0[0] - Ue_1[0]  # W = -AEp = Ue_0 - Ue_1

    assert compare_floats(3.393E-8, W)