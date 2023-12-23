
from sympy import Symbol
from .axes import Axes


class Vector:

    def __init__(self, name, dimensions=2, value=None):

        self.name = name
        self.dimensions = dimensions

        if dimensions != 2 and dimensions != 3:
            raise ValueError('Parameter \'dimensions\' must be 2 or 3')

        if value:

            if isinstance(value, (list, tuple)):
                if len(value) != self.dimensions:
                    raise ValueError(f'Value must have length \'{self.dimensions}\'')
            else:
                raise ValueError('Parameter \'value\' must be a list or tuple')

        self.axes = Axes(self.dimensions)
        self.value = tuple(value) if value else self._get_default_value()

    def __str__(self):

        return f'{self.name}_{self.dimensions}n'

    def __iter__(self):  # https://blog.finxter.com/python-__iter__-magic-method/
        
        self.current_index = 0
        
        return self

    def __next__(self):
        
        if self.current_index < len(self.value):

            value = self.value[self.current_index]
            self.current_index += 1
            return value
        
        raise StopIteration

    def __getitem__(self, idx):

        if idx >= self.dimensions:
            raise ValueError(f'Index {idx} out of range for Vector of length {len(self)}')

        return self.value[idx]
    
    def __setitem__(self, idx, value):

        if idx >= self.dimensions:
            raise ValueError(f'Index {idx} out of range for Vector of length {len(self)}')

        self.value = self.value[:idx] + (value,) + self.value[idx+1:]

    def __len__(self):

        return len(self.value)

    def __call__(self):

        return self.value

    def _get_default_value(self):

        output = tuple()
        
        for axis in self.axes.components.keys():
            output += (Symbol(self.name + '_' + axis),)

        return output

    def undefine(self, axis=None):

        if axis:
            
            if axis not in self.axes.components.keys():
                raise ValueError(f'Parameter \'axis\' must be one of these {self.axes.components.keys()}')
            
            idx = self.axes.components[axis]
            self[idx] = Symbol(self.name + '_' + axis)

        else:

            self.value = tuple()
        
            for axis in self.axes.components.keys():
                self.value += (Symbol(self.name + '_' + axis),)
    
    def define(self, value, axis=None):

        if axis:
            
            if axis not in self.axes.components.keys():
                raise ValueError(f'Parameter \'axis\' must be one of these {self.axes.components.keys()}')
            
            idx = self.axes.components[axis]
            self[idx] = value

        else:

            if not hasattr(value, '__len__') or len(value) != self.dimensions:
                raise ValueError(f'Parameter \'value\' must be of length {self.dimensions}')

            self.value = tuple(value)
        

