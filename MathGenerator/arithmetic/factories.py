import operator
import random

from MathGenerator.abstracts import ExerciseFactory


class ArithmeticFactory(ExerciseFactory):
    """Class for generating and solving arithmetic exercises"""
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
            components_count = 3 if level > 3 else 2
            components = [str(self.number_generator(1, max_number)) for _ in range(components_count)]
            question = self.operator_symbol.join(components)
            exercises.append(question)

        return exercises

    def solve(self, exercises: list) -> list:
        solutions = []
        for exercise in exercises:
            components = [int(component) for component in exercise.split(self.operator_symbol)]

            result = components[0]
            for component in components[1:]:
                result = self.operator_function(result, component)

            solutions.append(result)

        return solutions


class AdditionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="+", number_generator=random.randint)


class SubtractionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="-", number_generator=random.randint)


class MultiplicationFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="*", number_generator=random.randint)


class DivisionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator_symbol="/", number_generator=random.randint)


if __name__ == "__main__":
    generator = AdditionFactory()
    exercises = generator.generate(level=5, amount=10)
    results = generator.solve(exercises=exercises)

    print(f"Exercises: {exercises} \n Their solutions: {results}")
