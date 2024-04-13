import argparse
from MathGenerator.arithmetic import factories as arithmetic
from PDFGenerator.builder import Director, MathPDFBuilder


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
            'addition': arithmetic.AdditionFactory,
            'subtraction': arithmetic.SubtractionFactory,
            'multiplication': arithmetic.MultiplicationFactory,
            'division': arithmetic.DivisionFactory,
            'faddition': arithmetic.FractionAdditionFactory,
            'fsubtraction': arithmetic.FractionSubtractionFactory,
            'fmultiplication': arithmetic.FractionMultiplicationFactory,
            'fdivision': arithmetic.FractionDivisionFactory
        }
        return factories[operation]()


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
        'fdivision'],
                        required=True, help='Type of operation')
    parser.add_argument('-level', type=int, required=True, help='Difficulty level of the exercises')
    parser.add_argument('-amount', type=int, required=True, help='Amount of exercises to generate')

    args = parser.parse_args()

    # Initialize Factory based on passed argument
    factory = Factory.create(operation=args.operation)

    # Generate {args.amount} exercises
    exercises = factory.generate(level=args.level, amount=args.amount)

    # Solve above generated exercises
    solutions = factory.solve(exercises=exercises)

    # Initialize Director and his PDFBuilder
    director = Director()
    director.builder = MathPDFBuilder()

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
