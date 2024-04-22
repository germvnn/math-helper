from MathGenerator.abstracts import ExerciseFactory


class LinearFactory(ExerciseFactory):
    """Class for managing Linear exercises"""

    def __init__(self):
        super().__init__()

    def generate(self, level: int, amount: int):
        pass

    def solve(self, exercise):
        pass


class SingleLinearFactory(LinearFactory):
    """Base class for generating and solving single linear equations and inequalities"""

    def __init__(self, operator_symbol: str | None = None):
        super().__init__()
        self.operator = operator_symbol
        self.random_operator = True if self.operator is None else False


class SingleLinearEquationFactory(SingleLinearFactory):
    """Class for generating and solving single linear equations"""

    def __init__(self):
        super().__init__(operator_symbol="=")


class SingleLinearInequalityLessFactory(SingleLinearFactory):
    """Class for generating and solving single linear inequalities with 'less than' condition"""

    def __init__(self):
        super().__init__(operator_symbol="<")


class SingleLinearInequalityGreaterFactory(SingleLinearFactory):
    """Class for generating and solving single linear inequalities with 'greater than' condition"""

    def __init__(self):
        super().__init__(operator_symbol=">")


class SingleLinearEqualLessFactory(SingleLinearFactory):
    """Class for generating and solving single linear inequalities with 'greater than' condition"""

    def __init__(self):
        super().__init__(operator_symbol="<=")


class SingleLinearEqualGreaterFactory(SingleLinearFactory):
    """Class for generating and solving single linear inequalities with 'greater than' condition"""

    def __init__(self):
        super().__init__(operator_symbol=">=")


class LinearSystemFactory(LinearFactory):
    """Class for generating and solving systems of linear equations"""

    def __init__(self):
        super().__init__()


class LinearFunctionFactory(LinearFactory):
    """Class for generating and solving problems related to linear functions"""

    def __init__(self):
        super().__init__()
