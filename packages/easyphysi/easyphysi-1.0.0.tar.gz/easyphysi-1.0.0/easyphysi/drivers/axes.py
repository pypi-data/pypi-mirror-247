
class Axes:

    def __init__(self, dimensions):

        if dimensions != 2 and dimensions != 3:
            raise ValueError('Parameter \'dimensions\' must be 2 or 3')

        self.dimensions = dimensions
        self.components = {'x': 0, 'y': 1} if self.dimensions == 2 else {'x': 0, 'y': 1, 'z': 2}
