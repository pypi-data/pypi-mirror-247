import math

from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..drivers.system import System
from ..utils import distance, angle_with_horizontal_2d, angle_with_horizontal_3d, K


class ElectricalForceEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, name):

        return self.system(name)

    def _equation(self, main_body, axis):

        foo = 0.0

        # equation to solve is Fe_t - K*Q*Sum_i q_i/d_i**2  = 0
        
        for body in self.universe.bodies:
            if body is not main_body:
                
                # vector from body to main_body since we want to measure the angle between horizontal axis and main body

                if self.universe.dimensions == 2:
                    alpha = angle_with_horizontal_2d(body.position(), main_body.position())
                else:  # 3D
                    alpha, beta = angle_with_horizontal_3d(body.position(), main_body.position())

                dist = distance(body.position(), main_body.position())
                factor = math.cos(alpha) if axis == 0 else math.sin(alpha) if axis == 1 else math.sin(beta)
                foo -= K*main_body.charge()*body.charge()/dist**2 * factor

        foo += main_body.electrical_force[axis]
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['Fe', 'q', 'p']

        return ', '.join(sorted(parameters))

    def system(self, name):

        # INFO System / Equation cannot be solved for unknown 'p'

        body = self.universe.get_body(name)

        system = System()

        for axis, idx in self.axes.components.items():

            equation = self._equation(body, idx)
            system.add_equation(equation, key=axis)

        return system
