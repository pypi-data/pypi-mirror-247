
from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..drivers.system import System


class LinearPositionEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, name):

        return self.system(name)
        
    def _equation(self, body, axis):

        # equation to solve is p0-p + v0*t + 1/2*g*t**2 = 0
        
        foo = body.initial_position[axis] - body.position[axis] \
                    + body.initial_velocity[axis]*self.universe.time() \
                    + self.universe.gravity[axis]/2*self.universe.time()**2
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['p0','p', 'v0', 'g', 't']

        return ', '.join(sorted(parameters))

    def system(self, name):

        system = System()
        body = self.universe.get_body(name)

        for axis, idx in self.axes.components.items():

            equation = self._equation(body, idx)
            system.add_equation(equation, key=axis)

        return system