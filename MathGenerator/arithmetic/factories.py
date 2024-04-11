import random

from MathGenerator.abstracts import ExerciseFactory


class ArithmeticFactory(ExerciseFactory):
    """Class for generating and solving addition exercises"""
    def __init__(self, operator, number_generator):
        super().__init__()
        self.operator = f" {operator} "
        self.number_generator = number_generator

    def generate(self, level: int, amount: int):
        questions = []
        max_number = 10 ** level

        for _ in range(amount):
            components_count = 3 if level > 3 else 2
            components = [str(self.number_generator(1, max_number)) for _ in range(components_count)]
            question = self.operator.join(components)
            questions.append(question)

        return questions

    def solve(self, exercise: str):
        pass


class AdditionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator="+", number_generator=random.randint)


class SubtractionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator="-", number_generator=random.randint)


class MultiplicationFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator="*", number_generator=random.randint)


class DivisionFactory(ArithmeticFactory):
    def __init__(self):
        super().__init__(operator="/", number_generator=random.randint)


if __name__ == "__main__":
    generator = AdditionFactory()
    print(generator.generate(level=5, amount=5))