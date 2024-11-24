import random
import re

from MathGenerator.abstracts import ExerciseFactory

def format_terms(a, b, variable='x'):
    term_a = format_variable_term(a, variable)
    term_b = format_constant_term(b)

    if not term_a and not term_b:
        return "0"
    return f"{term_a}{term_b}".strip()


def format_variable_term(a, variable='x'):
    if a == 0:
        return ''
    elif a == 1:
        return f"{variable}"
    elif a == -1:
        return f"-{variable}"
    else:
        return f"{a}{variable}"


def format_constant_term(b):
    if b == 0:
        return ''
    sign = '-' if b < 0 else '+'
    return f" {sign} {abs(b)}"


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
            self.operator = random.choice(['=', '>', '<', '>=', '<=']) if self.random_operator else self.operator
            task_type = self._choose_task_type()

            if task_type == 'precise':
                a, b, c, d = self._generate_precise(level)
            elif task_type == 'identity':
                a, b, c, d = self._generate_identity(level)
            elif task_type == 'no solution':
                a, b, c, d = self._generate_no_solution(level)
            else:
                raise ValueError("Invalid task type")

            exercises.append(f"{format_terms(a, b)} {self.operator} {format_terms(c, d)}")
        return exercises

    def _generate_precise(self, level):
        a = self.number_generator(level)
        b = self.number_generator(level)
        c = self.number_generator(level)
        d = self.number_generator(level)
        while a == c:  # Avoid identity cases
            c = self.number_generator(level)
        return a, b, c, d

    def _generate_identity(self, level):
        a = self.number_generator(level)
        b = self.number_generator(level)
        return a, b, a, b

    def _generate_no_solution(self, level):
        a = self.number_generator(level)
        b = self.number_generator(level)
        c = a
        d = self.number_generator(level)
        while d == b:  # Ensure no solution
            d = self.number_generator(level)
        return a, b, c, d

    def _choose_task_type(self):
        if self.operator == '=':
            return random.choices(['precise', 'identity', 'no solution'], weights=[70, 10, 20])[0]
        return 'precise'

    def solve(self, exercises):
        solutions = {}
        for exercise in exercises:
            self.operator = re.search(r"(<=|>=|<|>|=)", exercise).group(0)
            left_side, right_side = exercise.split(f" {self.operator} ")

            a1, b1 = extract_coefficients(left_side)
            a2, b2 = extract_coefficients(right_side)

            a = a1 - a2
            b = b2 - b1

            solutions[exercise] = self._solve_linear(a, b)
        return solutions

    def _solve_linear(self, a, b):
        if a == 0:
            return 'identity (all x)' if b == 0 else 'no solution'

        x_solution = b / a if b / a != -0.0 else 0.0
        operator = reverse_operator(self.operator) if a < 0 else self.operator
        return f'x {operator} {x_solution}' if self.operator != '=' else f'x = {x_solution}'


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
