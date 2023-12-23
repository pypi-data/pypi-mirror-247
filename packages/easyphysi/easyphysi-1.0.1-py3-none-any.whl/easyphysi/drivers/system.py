import matplotlib.pyplot as plt

from sympy import solve, Symbol


class System:
    
    def __init__(self):

        self.equations = dict()
        self.unknowns = list()
        self.current_idx = 0

    def __getitem__(self, key):

        if not isinstance(key, str):
            raise ValueError('Parameter \'idx\' must be a string')
        
        if key not in self.equations.keys():
            raise ValueError(f'Key \'{key}\' not found in system with keys {self.equations.keys()}')

        return self.equations[key]

    def get_equation(self, key):

        return self[key]

    def add_equation(self, equation, key=None):

        if not hasattr(equation, 'function'):
            raise TypeError(f'Cannot add object of type {type(equation).__name__}')

        self.unknowns += [str(unknown) for unknown in equation.function.free_symbols]

        if key:
            self.equations[key] = equation
        else:
            self.equations[self.current_idx] = equation
            self.current_idx += 1

    def solve(self, unknowns):

        if not self.equations:
            raise RuntimeError('Before solving system you must add equations with \'add_equation\' method')

        for unknown in unknowns:

            if not isinstance(unknown, str):
                raise TypeError(f'Unknown must be str not {type(unknown).__name__}')
            
            if unknown not in self.unknowns:
                raise RuntimeError(f'Unknown \'{unknown}\' not in system unknowns {self.unknowns}')

        unknowns = [Symbol(unknown) for unknown in unknowns]
        functions = [equation.function for equation in self.equations.values()]  # dict order is preserved in python 3.6+
        solutions = solve(functions, unknowns, dict=True)

        if not solutions:
            raise ValueError('System solution not found')

        #let's move the roots of each unknown into a list to be consistent with Equation solutions

        roots = dict()

        for unknown in unknowns:
            roots[unknown] = list()
            for solution in solutions:
                roots[unknown].append(solution[unknown])

        return roots.values()

    def plot(self, independents, dependent, x_range, points=100, path=None, show=True):

        # Checks

        if not self.equations:
            raise RuntimeError('Before plotting system you must add equations with \'add_equation\' method')

        if len(independents) != len(self.equations):
            raise ValueError(f'Parameter \'independents\' must have length {len(self.equations)}, this is a vectorial equation')

        for axis, independent in zip(self.equations.keys(), independents):

            if len(self.equations[axis].unknowns) != 2:
                raise ValueError(f'Equation in axis \'{axis}\' must have exactly two unknowns, but it has ({self.equations[axis].unknowns})')
            
            if independent not in self.equations[axis].unknowns:
                raise ValueError(f'Independent unknown ({independent}) is not in equation in axis \'{axis}\' with unknowns ({self.equations[axis].unknowns})')

            if dependent not in self.equations[axis].unknowns:
                raise ValueError(f'Dependent unknown ({dependent}) is not in equation in axis \'{axis}\' with unknowns ({self.equations[axis].unknowns})')

        if len(x_range) != 2:
            raise ValueError('Parameter \'x_range\' must have length 2')

        # Solve for independent unknown

        functions = list()

        for axis, independent in zip(self.equations.keys(), independents):

            function = self.equations[axis].solve(independent)

            if not function:
                raise RuntimeError(f'Equation solution not found for {independent} unkown')

            if len(function) > 1:
                raise Warning(f'Several solutions found for {independent} unkown')

            functions.append(str(function[0]))

            # Get x,y points and plot

            dx = (x_range[1]-x_range[0]) / points
            x_list = [x_range[0]+dx*i for i in range(points)]
            y_list = [function[0].subs(dependent, x) for x in x_list]

            plt.plot(x_list, y_list)

        legend = [f'{independent} = {function}' for independent, function in zip(independents, functions)]

        plt.legend(legend)
        plt.xlabel(dependent)
        plt.ylabel(', '.join(independents))
        plt.grid()

        if path:
            plt.savefig(path)

        if show:
            plt.show()
