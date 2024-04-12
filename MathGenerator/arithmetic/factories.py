import operator
import random

from MathGenerator.abstracts import ExerciseFactory


class ArithmeticFactory(ExerciseFactory):
    """Class for generating and solving arithmetic exercises"""

    number_type = int
    result_format = staticmethod(lambda x: x)

    def __init__(self, operator_symbol, number_generator):
        super().__init__()
        self.operator_symbol = f" {operator_symbol} "
        self.operator_function = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }[operator_symbol]
        self.number_generator = number_generator

    def generate(self, level: int, amount: int) -> list:
        exercises = []
        max_number = 10 ** level

        for _ in range(amount):
            components_count = 3 if level > 4 else 2
            components = [str(self.number_generator(random.randint(2, 9), max_number)) for _ in range(components_count)]
            question = self.operator_symbol.join(components)
            exercises.append(question)

        return exercises

    def solve(self, exercises: list) -> dict:
        solutions = {}
        for exercise in exercises:
            components = [self.number_type(component) for component in exercise.split(self.operator_symbol)]

            result = components[0]
            for component in components[1:]:
                result = self.operator_function(result, component)

            solutions[exercise] = self.result_format(result)

        return solutions


class AdditionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="+", number_generator=random.randint)


class SubtractionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="-", number_generator=random.randint)


class MultiplicationFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="*", number_generator=lambda a, b: random.randint(a, round((b / 5) + a)))


class DivisionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="/", number_generator=random.randint)

    def generate(self, level: int, amount: int) -> list:
        exercises = []
        max_number = 10 ** level

        for _ in range(amount):
            dividend = self.number_generator(1, max_number)
            divisor = self.number_generator(1, 9) if level < 4 else self.number_generator(11, 99)
            exercise = f"{dividend}{self.operator_symbol}{divisor}"
            exercises.append(exercise)

        return exercises


class FractionFactory(ArithmeticFactory):

    number_type = float
    result_format = staticmethod(lambda x: round(x, 3))


class FractionAdditionFactory(FractionFactory, AdditionFactory):

    def __init__(self):
        super().__init__()
        self.number_generator = lambda a, b: random.randint(a, b) / 100


class FractionSubtractionFactory(FractionFactory, SubtractionFactory):

    def __init__(self):
        super().__init__()
        self.number_generator = lambda a, b: random.randint(a, b) / 100


class FractionMultiplicationFactory(FractionFactory, MultiplicationFactory):

    def __init__(self):
        super().__init__()
        self.number_generator = lambda a, b: random.randint(a, b) / 10


class FractionDivisionFactory(FractionFactory, DivisionFactory):

    def __init__(self):
        super().__init__()
        self.number_generator = lambda a, b: random.randint(a, b) / 10


if __name__ == "__main__":
    generator = FractionAdditionFactory()
    examples = generator.generate(level=1, amount=10)
    results = generator.solve(exercises=examples)

    print(f"Exercises: {examples} \nTheir solutions: {results}")
