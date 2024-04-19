import argparse
from MathGenerator.arithmetic import factories as arithmetic
import MathGenerator.algebra.quadratic as quadratic
from PDFGenerator.builder import Director, ArithmeticPDFBuilder, QuadraticPDFBuilder


class Factory:

    @staticmethod
    def create(operation):
        """
        Static method to create a factory object
        based on the type of arithmetic operation.

        Parameters:
        - operation (str): The type of arithmetic operation for which the factory is created.

        Returns:
        - An instance of the requested factory class.
        """
        factories = {
            'addition': (arithmetic.AdditionFactory, ArithmeticPDFBuilder),
            'subtraction': (arithmetic.SubtractionFactory, ArithmeticPDFBuilder),
            'multiplication': (arithmetic.MultiplicationFactory, ArithmeticPDFBuilder),
            'division': (arithmetic.DivisionFactory, ArithmeticPDFBuilder),
            'faddition': (arithmetic.FractionAdditionFactory, ArithmeticPDFBuilder),
            'fsubtraction': (arithmetic.FractionSubtractionFactory, ArithmeticPDFBuilder),
            'fmultiplication': (arithmetic.FractionMultiplicationFactory, ArithmeticPDFBuilder),
            'fdivision': (arithmetic.FractionDivisionFactory, ArithmeticPDFBuilder),
            'paddition': (arithmetic.PercentAdditionFactory, ArithmeticPDFBuilder),
            'psubtraction': (arithmetic.PercentSubtractionFactory, ArithmeticPDFBuilder),
            'quadraticrandom': (quadratic.QuadraticFactory, QuadraticPDFBuilder),
            'qequation': (quadratic.QuadraticEquationFactory, QuadraticPDFBuilder),
            'qinequationl': (quadratic.QuadraticInequalityLessFactory, QuadraticPDFBuilder),
            'qinequationg': (quadratic.QuadraticInequalityGreaterFactory, QuadraticPDFBuilder),
            'qequalless': (quadratic.QuadraticEqualLessFactory, QuadraticPDFBuilder),
            'qequalgreater': (quadratic.QuadraticEqualGreaterFactory, QuadraticPDFBuilder)
        }
        factory_class, builder_class = factories[operation]
        return factory_class(), builder_class()


def main():
    """
    Main function to handle command-line arguments and
    generate arithmetic exercises along with their solutions.

    It creates exercise and solution PDFs using the specified
    arithmetic operation, difficulty level, and amount.
    """

    parser = argparse.ArgumentParser(description="Arithmetic Exercise Generator")
    parser.add_argument('-operation', choices=[
        'addition',
        'subtraction',
        'multiplication',
        'division',
        'faddition',
        'fsubtraction',
        'fmultiplication',
        'fdivision',
        'paddition',
        'psubtraction',
        'quadraticrandom',
        'qequation',
        'qinequationl',
        'qinequationg',
        'qequalless',
        'qequalgreater'],
                        required=True, help='Type of operation')
    parser.add_argument('-level', type=int, required=True, help='Difficulty level of the exercises')
    parser.add_argument('-amount', type=int, required=True, help='Amount of exercises to generate')

    args = parser.parse_args()

    # Initialize Factory based on passed argument
    factory, builder = Factory.create(operation=args.operation)

    # Generate {args.amount} exercises
    exercises = factory.generate(level=args.level, amount=args.amount)

    # Solve above generated exercises
    solutions = factory.solve(exercises=exercises)

    # Initialize Director and his PDFBuilder
    director = Director()
    director.builder = builder

    # Create PDF based on generated exercises
    director.build_exercises(title=f"Exercises from {factory.__class__.__name__}",
                             exercises=exercises,
                             filename="exercises")

    # Create PDF based on solutions of above exercises
    director.build_solutions(title=f"Solutions from {factory.__class__.__name__}",
                             exercises=solutions,
                             filename=f"solutions")


if __name__ == "__main__":
    main()
