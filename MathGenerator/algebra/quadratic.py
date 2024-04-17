import math
import random
import re

from MathGenerator.abstracts import ExerciseFactory


class QuadraticFactory(ExerciseFactory):
    """Class for managing Quadratic exercises"""
    def __init__(self, operator_symbol):
        super().__init__()
        self.operator_symbol = operator_symbol

    def generate(self, level, amount):
        exercises = []
        # Process of generating single quadratic exercise
        for _ in range(amount):
            while True:
                a = random.randint(-level, level)
                # Making sure that equation will not be linear
                while a == 0:
                    a = random.randint(-level, level)

                b = random.randint(-3 * level, 3 * level)

                # Excluding 'easy' deltas from higher levels
                if level >= 5:
                    delta = random.choice([d for d in range(1, level ** 2 + 1) if int(math.sqrt(d)) ** 2 != d])
                else:
                    delta = random.choice([d ** 2 for d in range(level, level + 3)])

                c = (b ** 2 - delta) / (4 * a)
                # TODO: Temporary solution. Fractions have to be implemented
                if c.is_integer():
                    a_str = f"{'-' if a == -1 else '' if a == 1 else a}"
                    exercises.append(f"{a_str}x^2 + {b}x + {int(c)} {self.operator_symbol} 0")
                    break  # Leave while True if c is an integer

        return exercises

    def solve(self, exercises: list) -> dict:
        solutions = {}

        # Process of solving single exercise
        for exercise in exercises:
            # Prepare exercise string for regular expression
            clean_exercise = exercise.replace(" ", "").replace(f"{self.operator_symbol}0", "")
            # Regular expression which looks up at a, b, c
            coeffs = re.findall(r'([+-]?\d*)x\^2|([+-]?\d*)x|([+-]?\d+)', clean_exercise)

            # Read factor from re findings
            a = int(coeffs[0][0] if coeffs[0][0] != '' and coeffs[0][0] != '+' and coeffs[0][0] != '-' else (
                '1' if coeffs[0][0] == '' or coeffs[0][0] == '+' else '-1'))
            b = int(coeffs[1][1] if coeffs[1][1] != '' and coeffs[1][1] != '+' and coeffs[1][1] != '-' else (
                '1' if coeffs[1][1] == '' or coeffs[1][1] == '+' else '-1'))
            c = int(coeffs[2][2] if coeffs[2][2] else 0)

            delta = b ** 2 - 4 * a * c

            # Calculate roots based on delta
            if delta > 0:
                x1 = round((-b + delta ** 0.5) / (2 * a), 4)
                x2 = round((-b - delta ** 0.5) / (2 * a), 4)
                roots = (x1, x2)
            elif delta == 0:
                x1 = round(-b / (2 * a), 4)
                roots = (x1,)
            else:
                roots = "No real roots, complex roots present"

            # Append full solution to solutions dict
            solutions[exercise] = {
                "roots": roots,
                "parabola_direction": "up" if a > 0 else "down",
                "delta": delta
            }

        return solutions


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


class QuadraticEqualLessFactory(QuadraticFactory):
    """Quadratic Inequalities (less) or equal"""
    def __init__(self):
        super().__init__(operator_symbol='<=')


class QuadraticEqualGreaterFactory(QuadraticFactory):
    """Quadratic Inequalities (less) or equal"""
    def __init__(self):
        super().__init__(operator_symbol='>=')


if __name__ == "__main__":
    # factory = QuadraticEquationFactory()
    # factory = QuadraticInequalityLessFactory()
    factory = QuadraticInequalityGreaterFactory()
    exe = factory.generate(level=2, amount=5)
    sol = factory.solve(exercises=exe)
    print(f"exercises: {exe}")
    print(f"solutions: {sol}")
