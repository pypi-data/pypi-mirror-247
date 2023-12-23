import matplotlib.pyplot as plt

from sympy import Eq, solve


class Equation:

    def __init__(self, function, rhs=0.0):

        self.function = Eq(function, rhs)
        self.unknowns = [str(unknown) for unknown in self.function.free_symbols]

    def solve(self, unknown):
        
        if unknown not in self.unknowns:
            raise ValueError(f'Unknown \'{unknown}\' not in equation unknowns {self.unknowns}')

        roots = solve(self.function, unknown)

        return roots

    def plot(self, independent, dependent, x_range, points=100, path=None, show=True):

        # Checks
        
        if len(self.unknowns) != 2:
            raise ValueError(f'Equation must have exactly two unknowns, but it has ({self.unknowns})')

        if independent not in self.unknowns:
            raise ValueError(f'Independent unknown ({independent}) is not in equation unknowns ({self.unknowns})')

        if dependent not in self.unknowns:
            raise ValueError(f'Dependent unknown ({dependent}) is not in equation unknowns ({self.unknowns})')

        if len(x_range) != 2:
            raise ValueError('Parameter \'x_range\' must have length 2')

        # Solve for independent unknown

        function = self.solve(independent)

        if not function:
            raise RuntimeError(f'Equation solution not found for {independent} unkown')

        if len(function) > 1:
            Warning(f'Several solutions found for {independent} unkown')

        # Get x,y points and plot

        dx = (x_range[1]-x_range[0]) / points
        x_list = [x_range[0]+dx*i for i in range(points)]
        y_list = [function[0].subs(dependent, x) for x in x_list]

        plt.plot(x_list, y_list)

        plt.title(f'{independent} = ' + str(function[0]))
        plt.xlabel(dependent)
        plt.ylabel(f'{independent}')
        plt.grid()

        if path:
            plt.savefig(path)

        if show:
            plt.show()
