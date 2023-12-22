from scipy.constants import G

from ..drivers.axes import Axes
from ..drivers.equation import Equation
from ..utils import distance


class GravitationalPotentialEnergyEquation:
    
    def __init__(self, universe):

        self.universe = universe
        self.axes = Axes(self.universe.dimensions)

    def __call__(self, name):

        return self.equation(name)

    def _equation(self, main_body):

        foo = 0.0

        # https://physics.stackexchange.com/questions/578071/gravitational-potential-energy-of-an-n-body
        # 
        # The gravitational potential energy of a mass in a gravitational field is defined as the work 
        # done in bringing the mass from infinity to a point without changing its kinetic energy.
        # For n bodies, you bring the bodies one by one, so for the kth body, the cost (Ep) of bringing
        # it is Ep_k = Sum_i^k-1 Ep_i. If we have n bodies:
        #
        # Body   Ep
        # ==============
        # 0      0
        # 1      Ep_01
        # 2      Ep_02+Ep_12
        # ...
        # n      Ep_0n+Ep_1n+...+Ep_n-1,n
        #
        # The Ep for the whole system is the sum: Ep_01+Ep_02+Ep_12+...+Ep_0n+Ep_1n+...+Ep_n-1,n,
        # which is: Ep_t = Sum_i^n-1 Sum_j=i+1^n Ep_ij

        # equation to solve is Ug_t + G*Sum_i M_i*Sum_j=i+1 m_j/d_j = 0
        
        for idx, body_0 in enumerate(self.universe.bodies[:-1]):
            for body_1 in self.universe.bodies[idx+1:]:
                
                dist = distance(body_0.position(), body_1.position())
                foo += G*body_0.mass()*body_1.mass()/dist
        
        foo += main_body.gravitational_potential_energy()
        
        return Equation(foo)

    @property
    def parameters(self):

        parameters = ['Ug', 'm', 'p']

        return ', '.join(sorted(parameters))

    def equation(self, name):

        body = self.universe.get_body(name)
        equation = self._equation(body)

        return equation
