import math
from scipy.constants import G

from .body import Body
from .vector import Vector
from .scalar import Scalar
from ..equations.linear_position_equation import LinearPositionEquation
from ..equations.linear_velocity_equation import LinearVelocityEquation
from ..equations.newton_equation import NewtonEquation
from ..equations.energy_conservation_equation import EnergyConservationEquation
from ..equations.gravitational_force_equation import GravitationalForceEquation
from ..equations.gravitational_potential_energy_equation import GravitationalPotentialEnergyEquation
from ..equations.gravitational_field_intensity_equation import GravitationalFieldIntensityEquation
from ..equations.gravitational_potential_equation import GravitationalPotentialEquation
from ..equations.electrical_force_equation import ElectricalForceEquation
from ..equations.electrical_potential_energy_equation import ElectricalPotentialEnergyEquation
from ..equations.electrical_field_intensity_equation import ElectricalFieldIntensityEquation
from ..equations.electrical_potential_equation import ElectricalPotentialEquation
from ..utils import distance


class Universe:

    def __init__(self, dimensions=2):

        if dimensions != 2 and dimensions != 3:
            raise ValueError('Parameter \'dimensions\' must be 2 or 3')
        
        self.dimensions = dimensions

        self.bodies = list()

        # define universe properties

        self.electrical_field_intensity = Vector('Ee', self.dimensions)
        self.electrical_potential = Scalar('Ve')
        self.gravitational_field_intensity = Vector('gg', self.dimensions)  # this is the same as gravity 'g'
        self.gravitational_potential = Scalar('Vg')
        self.gravity = Vector('g', self.dimensions)
        self.time = Scalar('t')

        # define equations

        self.electrical_field_intensity_equation = ElectricalFieldIntensityEquation(self)
        self.electrical_force_equation = ElectricalForceEquation(self)
        self.electrical_potential_energy_equation = ElectricalPotentialEnergyEquation(self)
        self.electrical_potential_equation = ElectricalPotentialEquation(self)
        self.energy_conservation_equation = EnergyConservationEquation(self)
        self.gravitational_field_intensity_equation = GravitationalFieldIntensityEquation(self)
        self.gravitational_force_equation = GravitationalForceEquation(self)
        self.gravitational_potential_energy_equation = GravitationalPotentialEnergyEquation(self)
        self.gravitational_potential_equation = GravitationalPotentialEquation(self)
        self.linear_position_equation = LinearPositionEquation(self)
        self.linear_velocity_equation = LinearVelocityEquation(self)
        self.newton_equation = NewtonEquation(self)

    def add_body(self, body):

        if not isinstance(body, Body):
            raise TypeError(f'Cannot add object of type {type(body).__name__}')

        if body.dimensions != self.dimensions:
            raise ValueError(f'Body dimensions {body.dimensions} and universe dimensions {self.dimensions} mismatch')
        
        self.bodies.append(body)

    def get_body(self, name):

        body = [body for body in self.bodies if body.name == name]

        if not body:
            raise ValueError(f'Body with name {name} not found')
        
        return body[0]

    def short_to_long(self, short):

        for long, obj in self.__dict__.items():

            if isinstance(obj, (Vector, Scalar)):
                if obj.name == short:
                    return long

        return None

    def set(self, name, value):

        axis = None

        # get axis and remove it from name

        if name.endswith(('_x', '_y', '_z')):
            name, axis = name[:-2], name[-1]

        property_ = self.short_to_long(name)

        if not hasattr(self, property_):

            self._help_properties()
            raise ValueError(f'Property \'{property_}\' not found, see allowed properties in table above')
        
        unknown = getattr(self, property_)

        if isinstance(unknown, Vector):
            unknown.define(value, axis=axis)
        else:
            unknown.define(value)

    def unset(self, name):

        axis = None

        # get axis and remove it from name

        if name.endswith(('_x', '_y', '_z')):
            name, axis = name[:-2], name[-1]

        property_ = self.short_to_long(name)

        if not hasattr(self, property_):

            self._help_properties()
            raise ValueError(f'Property \'{property_}\' not found, see allowed properties in table above')
        
        unknown = getattr(self, property_)
        
        if isinstance(unknown, Vector):
            unknown.undefine(axis=axis)
        else:
            unknown.undefine()

    def _help_properties(self):

        print('')
        print('The following properties are allowed:')
        print('')
        print(' {:10s} {:32s} {:10s} {:16s}'.format('Property', 'Description', 'Type', 'Value'))
        print(' ' + '='*10 + ' ' + '='*32 + ' '+ '='*10 + ' '+ '='*16)

        for key, value in self.__dict__.items():

            if isinstance(value, (Vector, Scalar)):
                description = key[0].upper() + key[1:].replace('_', ' ')
                print(f' {value.name:10s} {description:32s} {type(value).__name__:10s} {value.value}')

        print('')

    def _help_equations(self):

        print('')
        print('The following equations are allowed:')
        print('')
        print(' {:40s} {:10s} {:16s}'.format('Equation', 'Type', 'Parameters'))
        print(' ' + '='*40 + ' ' + '='*10 + ' '+ '='*16)

        for key, value in self.__dict__.items():

            if hasattr(value, '_equation'):
                type_ = 'Scalar' if hasattr(value, 'equation') else 'Vectorial'
                print(f' {key:40s} {type_:10s} {value.parameters}')

        print('')

    def help(self):

        self._help_properties()
        self._help_equations()
