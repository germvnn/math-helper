from MathGenerator.abstracts import ExerciseFactory


class QuadraticFactory(ExerciseFactory):
    """Class for managing Quadratic exercises"""
    def __init__(self, operator_symbol):
        super().__init__()
        self.operator_symbol = operator_symbol

    def generate(self, level: int, amount: int):
        pass

    def solve(self, exercise):
        pass


class QuadraticEquationFactory(QuadraticFactory):
    """Quadratic Equations"""
    def __init__(self):
        super().__init__(operator_symbol='=')


class QuadraticInequalityLessFactory(QuadraticFactory):
    """Quadratic Inequalities (less)"""
    def __init__(self):
        super().__init__(operator_symbol='<')


class QuadraticInequalityGreaterFactory(QuadraticFactory):
    """Quadratic Inequalities (greater)"""
    def __init__(self):
        super().__init__(operator_symbol='>')
