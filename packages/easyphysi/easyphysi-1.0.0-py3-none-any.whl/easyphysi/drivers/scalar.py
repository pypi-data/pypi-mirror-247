
from sympy import Symbol

from ..utils import none_type


class Scalar:

    def __init__(self, name, value=None):

        self.name = name

        self.value = self._get_default_value() if isinstance(value, none_type) else value

    def __str__(self):

        return self.name

    def __call__(self):

        return self.value

    def _get_default_value(self):

        return Symbol(self.name)

    def undefine(self):

        self.value = self._get_default_value()
    
    def define(self, value):

        self.value = value 
