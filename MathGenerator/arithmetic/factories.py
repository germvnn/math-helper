import operator
import random

from MathGenerator.abstracts import ExerciseFactory


class ArithmeticFactory(ExerciseFactory):
    """
    A class for generating and solving arithmetic exercises, supporting basic
    arithmetic operations such as addition, subtraction, multiplication, and division.

    Attributes:
        number_type (type): The data type for the components of arithmetic expressions,
                            default is int.
        result_format (function): A static method that formats the output of calculations.
                                  By default, it returns the result unchanged.
        number_generator (function): A function to generate integer numbers. By default,
                                     it uses random.randint.
        operator_symbol (str): The symbol of the operator used to create exercises.
        operator_function (dict): A dictionary mapping operator symbols to corresponding
                                  arithmetic functions (operator.add, operator.sub,
                                  operator.mul, operator.truediv).

    Methods:
        __init__(self, operator_symbol):
            Initializes the ArithmeticFactory with the specified operator symbol.

        generate(self, level: int, amount: int) -> list:
            Generates a list of arithmetic exercises. The complexity and quantity of
            exercises are determined by the `level` and `amount` parameters.
            - level (int): The difficulty level of the exercises, affecting the maximum
                           numbers used in exercises.
            - amount (int): The number of exercises to generate.

        solve(self, exercises: list) -> dict:
            Solves a list of arithmetic exercises provided in `exercises`. Returns a
            dictionary where keys are the exercises and values are the solutions.
            - exercises (list): A list of string expressions representing the arithmetic
                                problems to solve.
    """
    # Describes types of numbers in exercises
    number_type: type = int
    # Format results of solve method
    result_format = staticmethod(lambda x: x)

    number_generator = random.randint

    def __init__(self, operator_symbol):
        super().__init__()
        self.operator_symbol = f" {operator_symbol} "
        self.operator_function = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }[operator_symbol]

    def generate(self, level: int, amount: int) -> list:
        # Initialize an empty list of exercises
        exercises = []
        max_number = 10 ** level

        # Process of generating a single exercise
        for _ in range(amount):
            components_count = 3 if level > 4 else 2
            components = [str(
                self.number_generator(random.randint(2, 9), max_number)
            ) for _ in range(components_count)]
            exercise = self.operator_symbol.join(components)
            exercises.append(exercise)

        return exercises

    def solve(self, exercises: list) -> dict:
        # Initialize an empty dict of solutions {'exercise': solution}
        solutions = {}

        # Process of solving a single exercise
        for exercise in exercises:
            components = [self.number_type(component) for component in exercise.split(self.operator_symbol)]

            result = components[0]
            for component in components[1:]:
                result = self.operator_function(result, component)

            solutions[exercise] = self.result_format(result)

        return solutions


class AdditionFactory(ArithmeticFactory):
    """Class for managing Addition exercises"""
    def __init__(self):
        super().__init__(operator_symbol="+")


class SubtractionFactory(ArithmeticFactory):
    """Class for managing Subtraction exercises"""
    def __init__(self):
        super().__init__(operator_symbol="-")


class MultiplicationFactory(ArithmeticFactory):
    """Class for managing Multiplication exercises"""

    # Set other generator to adjust difficulty
    number_generator = staticmethod(lambda a, b: random.randint(a, round((b / 5) + a)))

    def __init__(self):
        super().__init__(operator_symbol="*")


class DivisionFactory(ArithmeticFactory):
    """Class for managing Division exercises"""
    # TODO: Consider implementing modulo in solutions
    # Rounding results to three decimal places
    result_format = staticmethod(lambda x: round(x, 3))

    def __init__(self):
        super().__init__(operator_symbol="/")

    # Override generate method to achieve smaller divisor
    def generate(self, level: int, amount: int) -> list:
        exercises = []
        max_number = 10 ** level

        # Process of generating a single division exercise
        for _ in range(amount):
            dividend = self.number_generator(1, max_number)
            divisor = self.number_generator(1, 9) if level < 4 else self.number_generator(11, 99)
            exercise = f"{dividend}{self.operator_symbol}{divisor}"
            exercises.append(exercise)

        return exercises


class FractionFactory(ArithmeticFactory):
    """Subclass for managing Fractions operations"""
    number_type = float

    # Situations like 1 + 2 = 2.9999999997 avoidance
    result_format = staticmethod(lambda x: round(x, 3))
    number_generator = staticmethod(lambda a, b: random.randint(a, b) / 100)


""" These are self-explanatory"""


class FractionAdditionFactory(FractionFactory, AdditionFactory):
    pass


class FractionSubtractionFactory(FractionFactory, SubtractionFactory):
    pass


class FractionMultiplicationFactory(FractionFactory, MultiplicationFactory):
    number_generator = staticmethod(lambda a, b: random.randint(a, b) / 10)


class FractionDivisionFactory(FractionFactory, DivisionFactory):
    number_generator = staticmethod(lambda a, b: random.randint(a, b) / 10)


class PercentFactory(ArithmeticFactory):
    number_type = float
    number_generator = staticmethod(lambda a, precision: round(random.uniform(a, 100), precision))
    result_format = staticmethod(lambda x, dp: round(x, dp))

    def generate(self, level: int, amount: int) -> list:
        exercises = []
        max_number = 100  # Percentages

        # Process of generating single exercise
        for _ in range(amount):
            components_count = 3 if level > 4 else 2
            components = [
                f"{self.number_generator(a=random.randint(2, 9), precision=level - 1)}%"
                for _ in range(components_count)
            ]
            exercise = self.operator_symbol.join(components)
            exercises.append(exercise)
        return exercises

    def solve(self, exercises: list) -> dict:
        solutions = {}

        # Process of solving a single exercise
        for exercise in exercises:
            # Remove the '%' sign
            components = [component.replace('%', '') for component in
                          exercise.split(self.operator_symbol)]
            # Check max number of decimal places for components
            dp = max((component[::-1].find('.') for component in components if '.' in component), default=0)
            # Convert components to numeric type
            components = [self.number_type(component) for component in components]
            result = components[0]
            for component in components[1:]:
                result = self.operator_function(result, component)
            # Format the result to add the '%' sign and store it in the solutions dictionary
            solutions[exercise] = f"{self.result_format(result, dp)}%"

        return solutions


class PercentAdditionFactory(PercentFactory, AdditionFactory):
    pass


class PercentSubtractionFactory(PercentFactory, SubtractionFactory):
    pass


class PercentMultiplicationFactory(PercentFactory, MultiplicationFactory):
    # TODO: Adjust generate method by new 'level mechanism' due to difficulty
    # TODO: Implement solve method adjusted to percentages.
    pass


if __name__ == "__main__":
    generator = PercentSubtractionFactory()
    examples = generator.generate(level=1, amount=10)
    results = generator.solve(exercises=examples)

    print(f"Exercises: {examples} \nTheir solutions: {results}")
