
from ..drivers.axes import Axes
from ..drivers.equation import Equation


class EnergyConservationEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, name):

        return self.equation(name)

    def _equation(self, body):

        foo = 0.0

        # equation to solve is \sum E = 0
        
        for energy in body.energies:
            foo += energy()
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = []

        return ', '.join(sorted(parameters))

    def equation(self, name):

        body = self.universe.get_body(name)

        if not body.energies:
            raise ValueError('Before solving the equation you must add energy(ies) over body with \'add_energy\' method')

        equation = self._equation(body)

        return equation
