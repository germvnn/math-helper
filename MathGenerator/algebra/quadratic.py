import math
import random
import re
from typing import List, Dict, Union, Tuple

from MathGenerator.abstracts import ExerciseFactory


class QuadraticFactory(ExerciseFactory):
    """Class for managing Quadratic exercises"""
    def __init__(self, operator_symbol: str | None = None):
        super().__init__()
        self.operator = operator_symbol
        self.random_operator = self.operator is None

    def generate(self, level: int, amount: int) -> list[str]:
        return [self._generate_single_exercise(level) for _ in range(amount)]

    def _generate_single_exercise(self, level: int) -> str:
        operator = self._choose_operator()
        a = self._generate_a(level)
        b = self._generate_b(level)
        delta = self._generate_delta(level)
        c = self._calculate_c(a, b, delta)
        return self._format_equation(a, b, c, operator)

    def _choose_operator(self) -> str:
        return random.choice(['=', '>', '<', '>=', '<=']) if self.random_operator else self.operator

    @staticmethod
    def _generate_a(level: int) -> int:
        a = 0
        while a == 0:
            a = random.randint(-level, level)
        return a

    @staticmethod
    def _generate_b(level: int) -> int:
        return random.randint(-3 * level, 3 * level)

    @staticmethod
    def _generate_delta(level: int) -> int:
        if level >= 5:
            return random.choice([d for d in range(1, level ** 2 + 1) if int(math.sqrt(d)) ** 2 != d])
        delta = random.choice([d ** 2 for d in range(level, level + 3)])
        if random.choice([True, False]):
            delta *= -1 if random.choice([True, False]) else 0
        return delta

    @staticmethod
    def _calculate_c(a: int, b: int, delta: int) -> float:
        return (b ** 2 - delta) / (4 * a)

    @staticmethod
    def _format_equation(a: int, b: int, c: float, operator: str) -> str:
        a_str = f"{'-' if a == -1 else '' if a == 1 else a}x^2"
        b_str = f" + {b}x" if b >= 0 else f" - {-b}x"
        c_str = f" + {c}" if c >= 0 else f" - {-c}"
        return f"{a_str}{b_str}{c_str} {operator} 0"

    def solve(self, exercises: List[str]) -> Dict[str, Dict[str, Union[Tuple, str, float]]]:
        solutions = {}
        for exercise in exercises:
            try:
                a, b, c = self._extract_coefficients(exercise)
                delta = self._calculate_delta(a, b, c)
                roots = self._calculate_roots(a, b, delta)
                parabola_direction = "up" if a > 0 else "down"

                solutions[exercise] = {
                    "roots": roots,
                    "parabola_direction": parabola_direction,
                    "delta": delta
                }
            except ValueError as e:
                solutions[exercise] = {"error": str(e)}

        return solutions

    def _extract_coefficients(self, exercise: str) -> Tuple[float, float, float]:
        clean_exercise = exercise.replace(" ", "").replace(f"{self.operator}0", "")
        coeffs = re.findall(r'(-?\d*\.?\d+|[-+]?)x\^2|(-?\d*\.?\d+|[-+]?)x|(-?\d*\.?\d+)', clean_exercise)

        if len(coeffs) != 3:
            raise ValueError(f"Invalid quadratic equation format: {exercise}")

        a = self._parse_coefficient(coeffs[0][0])
        b = self._parse_coefficient(coeffs[1][1])
        c = float(coeffs[2][2]) if coeffs[2][2] else 0.0

        if a == 0:
            raise ValueError(f"Not a quadratic equation (a=0): {exercise}")

        return a, b, c

    def _parse_coefficient(self, value: str) -> float:
        if value in ['', '+']:
            return 1.0
        elif value == '-':
            return -1.0
        return float(value)

    def _calculate_delta(self, a: float, b: float, c: float) -> float:
        delta = b ** 2 - 4 * a * c
        return int(delta) if delta == int(delta) else delta

    def _calculate_roots(self, a: float, b: float, delta: float) -> Union[Tuple[float, ...], str]:
        if delta > 0:
            x1 = (-b + delta ** 0.5) / (2 * a)
            x2 = (-b - delta ** 0.5) / (2 * a)
            return round(x1, 5), round(x2, 5)
        elif delta == 0:
            x1 = -b / (2 * a)
            return round(x1, 5),
        else:
            return "No real roots, complex roots present"


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
