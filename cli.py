import argparse
from MathGenerator.arithmetic import factories as arithmetic
from PDFGenerator.builder import Director, MathPDFBuilder


class Factory:
    @staticmethod
    def create(operation):
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

    factory = Factory.create(operation=args.operation)
    exercises = factory.generate(level=args.level, amount=args.amount)
    solutions = factory.solve(exercises=exercises)

    director = Director()
    builder = MathPDFBuilder()
    director.builder = builder

    director.build_exercises(title=f"Exercises from {factory.__class__.__name__}",
                             exercises=exercises,
                             filename="exercises")

    director.build_solutions(title=f"Solutions from {factory.__class__.__name__}",
                             exercises=solutions,
                             filename=f"solutions")


if __name__ == "__main__":
    main()
