import math
import random
import re

from MathGenerator.abstracts import ExerciseFactory


class QuadraticFactory(ExerciseFactory):
    """Class for managing Quadratic exercises"""
    def __init__(self, operator_symbol: str | None = None):
        super().__init__()
        self.operator = operator_symbol
        self.random_operator = True if self.operator is None else False

    def generate(self, level: int, amount: int) -> list:
        # TODO: Parentheses for b, c < 0 temporary done in PDF utils.
        exercises = []
        # Process of generating single quadratic exercise
        for _ in range(amount):
            # Set random operator if not provided
            self.operator = random.choice(['=', '>', '<', '>=', '<=']) if self.random_operator else self.operator
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
                # 50% chance delta > 0 - 25% = 0 - 25% < 0
                if random.choice([True, False]):
                    delta *= -1 if random.choice([True, False]) else 0

            c = (b ** 2 - delta) / (4 * a)
            a_str = f"{'-' if a == -1 else '' if a == 1 else a}"
            exercises.append(f"{a_str}x^2 + {b}x + {c} {self.operator} 0")
            # Reset operator
            self.operator = None if self.random_operator else self.operator

        return exercises

    def solve(self, exercises: list) -> dict:
        # TODO: Adjust regexp for equations like x^2 + (-3)x + (-3) = 0
        solutions = {}

        # Process of solving single exercise
        for exercise in exercises:
            # Prepare exercise string for regular expression
            clean_exercise = exercise.replace(" ", "").replace(f"{self.operator}0", "")
            # Regular expression which looks up at a, b, c
            coeffs = re.findall(r'(-?\d*\.?\d*)x\^2|(-?\d*\.?\d*)x|(-?\d*\.?\d+)', clean_exercise)

            # Read factor from re findings
            a = int(coeffs[0][0] if coeffs[0][0] != '' and coeffs[0][0] != '+' and coeffs[0][0] != '-' else (
                '1' if coeffs[0][0] == '' or coeffs[0][0] == '+' else '-1'))
            b = int(coeffs[1][1] if coeffs[1][1] != '' and coeffs[1][1] != '+' and coeffs[1][1] != '-' else (
                '1' if coeffs[1][1] == '' or coeffs[1][1] == '+' else '-1'))
            c = float(coeffs[2][2] if coeffs[2][2] else 0)

            delta = b ** 2 - 4 * a * c
            # Format delta as integer if so
            delta = int(delta) if int(delta) - delta == 0 else delta

            # Calculate roots based on delta
            if delta > 0:
                x1 = (-b + delta ** 0.5) / (2 * a)
                x2 = (-b - delta ** 0.5) / (2 * a)
                roots = (x1, x2)
            elif delta == 0:
                x1 = -b / (2 * a)
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
    factory = QuadraticFactory()
    exe = factory.generate(level=2, amount=20)
    sol = factory.solve(exercises=exe)
    print(f"exercises: {exe}")
    print(f"solutions: {sol}")
