import math
import random

from MathGenerator.abstracts import ExerciseFactory


class QuadraticFactory(ExerciseFactory):
    """Class for managing Quadratic exercises"""
    def __init__(self, operator_symbol):
        super().__init__()
        self.operator_symbol = f" {operator_symbol} "

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

                if c.is_integer():
                    a_str = f"{'-' if a == -1 else '' if a == 1 else a}"
                    exercises.append(f"{a_str}x^2 + {b}x + {int(c)}{self.operator_symbol}0")
                    break  # Leave while True if c is an integer

        return exercises

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


if __name__ == "__main__":
    # factory = QuadraticEquationFactory()
    factory = QuadraticInequalityLessFactory()
    exe = factory.generate(level=3, amount=10)
    print(f"exercises: {exe}")
