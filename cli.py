import argparse
from MathGenerator.arithmetic import factories as arithmetic


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

    print(f"Generated Exercises: {exercises}")
    print(f"Their Solutions: {solutions}")


if __name__ == "__main__":
    main()
