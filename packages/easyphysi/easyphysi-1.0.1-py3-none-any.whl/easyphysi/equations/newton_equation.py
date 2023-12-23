
from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..drivers.system import System


class NewtonEquation:

    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, name):

        return self.system(name)

    def _equation(self, body, axis):

        foo = 0.0

        # equation to solve is \sum F - m*a = 0
        
        for force in body.forces:
            foo += force[axis]

        foo -= body.mass()*body.acceleration[axis]
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['m', 'a']

        return ', '.join(sorted(parameters))

    def system(self, name):

        system = System()
        body = self.universe.get_body(name)

        if not body.forces:
            raise ValueError('Before solving the equation you must add force(s) over body with \'add_force\' method')

        for axis, idx in self.axes.components.items():

            equation = self._equation(body, idx)
            system.add_equation(equation, key=axis)

        return system
