
from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..drivers.system import System


class LinearVelocityEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)
    
    def __call__(self, name):

        return self.system(name)

    def _equation(self, body, axis):

        # equation to solve is v0-v + g*t = 0
        
        foo = body.initial_velocity[axis] - body.velocity[axis] \
                    + self.universe.gravity[axis]*self.universe.time()

        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['v0', 'v', 'g', 't']

        return ', '.join(sorted(parameters))

    def system(self, name):

        system = System()
        body = self.universe.get_body(name)

        for axis, idx in self.axes.components.items():

            equation = self._equation(body, idx)
            system.add_equation(equation, key=axis)

        return system