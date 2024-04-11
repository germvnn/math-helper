from MathGenerator.abstracts import ExerciseFactory


class AdditionFactory(ExerciseFactory):
    """Class for generating and solving addition exercises"""
    def __init__(self):
        super().__init__()

    def generate(self, level: int, amount: int):
        pass

    def solve(self, exercise):
        pass
