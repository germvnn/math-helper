import random
import re

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


def extract_coefficients(expression: str):
    # Normalize expression by removing spaces and splitting at the relational operator
    expression = expression.replace(' ', '')

    # Enhanced regex to capture terms with x (including default coefficients) and constants
    coeffs = re.findall(r'([+-]?\d*\.?\d*)x|([+-]?\d+\.?\d*)', expression)

    a = 0
    b = 0

    # Aggregate coefficients for x and constant terms
    found_x = False
    for coeff_pair in coeffs:
        if 'x' in expression and coeff_pair[0] != '':
            if coeff_pair[0] == '-':
                a -= 1
            else:
                a += float(coeff_pair[0])
            found_x = True
        if coeff_pair[1]:  # Constant term
            b += float(coeff_pair[1])

    # If 'x' is present in the expression but no coefficient has been assigned
    if 'x' in expression and not found_x:
        a = 1

    return a, b


def reverse_operator(operator):
    """ Reverse the inequality operator """
    if operator == '>':
        return '<'
    elif operator == '<':
        return '>'
    elif operator == '>=':
        return '<='
    elif operator == '<=':
        return '>='
    return operator


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

    # TODO: Consider fractions for higher levels
    def generate(self, level: int, amount: int):
        exercises = []
        for _ in range(amount):
            # Assign operator if not provided
            self.operator = random.choice(['=', '>', '<', '>=', '<=']) if self.random_operator else self.operator

            # TODO: Think about this solution
            if self.operator == '=':
                task_type = random.choices(
                    ['precise', 'identity', 'no solution'],
                    weights=[70, 10, 20],
                )[0]
            else:
                task_type = 'precise'

            a = self.number_generator(level)
            b = self.number_generator(level)

            # Match number generator based on task type
            match task_type:
                case 'precise':
                    c = self.number_generator(level)
                    d = self.number_generator(level)
                    while a == c:  # Make sure that exercise is not identity
                        c = self.number_generator(level)
                case 'identity':
                    c = a
                    d = b
                case 'no solution':
                    c = a
                    d = b
                    while d == b:  # Make sure that exercise has no solution
                        d = self.number_generator(level)
                case _:
                    raise ValueError("Invalid task type")
            exercises.append(f"{format_terms(a, b)} {self.operator} {format_terms(c, d)}")
            self.operator = None if self.random_operator else self.operator
        return exercises

    def solve(self, exercises):
        solutions = {}
        for exercise in exercises:

            self.operator = re.findall(r"(<=|>=|<|>|=)", exercise)[0]
            # Divide exercise by lef, right side
            parts = exercise.split(f" {self.operator} ")
            left_side, right_side = parts[0], parts[1]

            # Get coefficients values
            a1, b1 = extract_coefficients(''.join(left_side))
            a2, b2 = extract_coefficients(''.join(right_side))

            # Move ax to left_side, b to right_side
            a = a1 - a2
            b = b2 - b1

            if a == 0:
                if b == 0:
                    solutions[exercise] = 'identity (all x)'  # 0 = 0
                else:
                    solutions[exercise] = 'no solution'  # 0 = {non_zero_value}
            else:
                x_solution = b / a if b / a != -0.0 else 0.0  # I love operations on floats
                if self.operator == '=':
                    solutions[exercise] = f'x = {x_solution}'
                elif self.operator in ['>', '<', '>=', '<=']:
                    # Reverse the operator if A is negative
                    if a < 0:
                        solutions[exercise] = f'x {reverse_operator(self.operator)} {x_solution}'
                    else:
                        solutions[exercise] = f'x {self.operator} {x_solution}'
                else:
                    raise ValueError("Invalid operator")

        return solutions


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
    factory = SingleLinearFactory(operator_symbol="<=")
    exe = factory.generate(level=1, amount=15)
    sol = factory.solve(exe)
    print(f"Exercises: {exe}")
    print(f"Sol: {sol}")
