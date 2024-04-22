import random

from MathGenerator.abstracts import ExerciseFactory


def format_terms(a, b, variable='x'):
    """
    Formats the terms for an equation based on the provided coefficients.

    :param a: Coefficient for the variable term.
    :param b: Coefficient for the constant term.
    :param variable: The variable of the equation, default 'x'.
    :return: Formatted part of the equation as a string.
    """
    # Handle the variable term
    if a == 0:
        term_a = ''
    elif a == 1:
        term_a = f"{variable}"
    elif a == -1:
        term_a = f"-{variable}"
    else:
        term_a = f"{a}{variable}"

    # Handle the constant term
    if b == 0:
        term_b = ''
    else:
        sign = '-' if b < 0 else '+'
        abs_b = abs(b)
        term_b = f" {sign} {abs_b}"

    # Combine the terms
    if a == 0 and b == 0:
        return "0"
    elif a == 0:
        return f"{b}"
    elif b == 0:
        return term_a
    else:
        return f"{term_a}{term_b}"


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

    number_generator = staticmethod(lambda x: random.randint(-x * 3, x * 3))

    def __init__(self, operator_symbol: str | None = None):
        super().__init__()
        self.operator = operator_symbol
        self.random_operator = True if self.operator is None else False

    def generate(self, level: int, amount: int):
        exercises = []
        for _ in range(amount):
            # Assign operator if not provided
            self.operator = random.choice(['=', '>', '<', '>=', '<=']) if self.random_operator else self.operator

            task_type = random.choices(
                ['precise', 'identity', 'no solution'],
                weights=[60, 20, 20],
            )[0]

            # Match number generator based on task type
            match task_type:
                case 'precise':
                    a = self.number_generator(level)
                    b = self.number_generator(level)
                    c = self.number_generator(level)
                    d = self.number_generator(level)

                    # Make sure that exercise is not identity
                    while a == c:
                        c = self.number_generator(level)

                case 'identity':
                    a = self.number_generator(level)
                    b = self.number_generator(level)
                    c = a
                    d = b

                case 'no solution':
                    a = self.number_generator(level)
                    b = self.number_generator(level)
                    c = a
                    d = b
                    while d == b:
                        d = self.number_generator(level)

                case _:
                    raise ValueError("Invalid task type")
            exercises.append(f"{format_terms(a, b)} {self.operator} {format_terms(c, d)}")
            self.operator = None if self.random_operator else self.operator
        return exercises


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


if __name__ == "__main__":
    factory = SingleLinearEquationFactory()
    exe = factory.generate(level=10, amount=15)
    print(f"Exercises: {exe}")
