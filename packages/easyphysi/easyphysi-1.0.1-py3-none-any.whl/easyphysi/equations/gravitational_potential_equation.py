from scipy.constants import G

from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..utils import distance


class GravitationalPotentialEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, point):

        return self.equation(point)

    def _equation(self, point):

        foo = 0.0

        # equation to solve is Vg_t + G*Sum_i m_i/d_i  = 0
        
        for body in self.universe.bodies:
                
            dist = distance(body.position(), point)
            foo += G*body.mass()/dist

        foo += self.universe.gravitational_potential()
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['Vg', 'm', 'p']

        return ', '.join(sorted(parameters))

    def equation(self, point):

        if not hasattr(point, '__len__') or len(point) != self.universe.dimensions:
            raise ValueError(f'Parameter \'point\' must have length {self.universe.dimensions}')
        
        equation = self._equation(point)

        return equation
