import pytest
import random
import re

from MathGenerator.algebra import quadratic as q


@pytest.mark.parametrize("factory_class, level", [
    (q.QuadraticEquationFactory, 2),
    (q.QuadraticInequalityLessFactory, 2),
    (q.QuadraticInequalityGreaterFactory, 2),
])
def test_quadratic_generate(factory_class, level):
    factory = factory_class()
    amount = random.randint(1, 10)  # Generate a random number of exercises to create
    exercises = factory.generate(level=level, amount=amount)

    assert len(exercises) == amount, f"Generated {len(exercises)} exercises, expected {amount}"

    for exercise in exercises:
        assert factory.operator_symbol in exercise, f"Operator {factory.operator_symbol} not found in {exercise}"

        # Assuming the quadratic exercise is structured like 'ax^2 + bx + c operator 0'
        components = exercise.split(factory.operator_symbol)

        assert components[1] is '0'
        left_side = components[0]  # Only one side as the other is assumed to be '0'

        # Count all occurrences of x
        all_x = re.findall(r'x', left_side)
        # Count only x^2
        x_squared = re.findall(r'x\^2', left_side)

        assert len(x_squared) == 1, "Should be exactly one 'x^2' term."
        # Since each x^2 includes two x's, adjust the count of single x's
        assert len(all_x) - len(x_squared) == 1, "Should be exactly one 'x'"


@pytest.mark.parametrize("factory_class, test_input, expected_output", [
    (q.QuadraticEquationFactory, "x^2 - 5x + 6 = 0",
     {"exercise": "x^2 - 5x + 6 = 0", "x1": 2, "x2": 3, "parabola_up": True}),
    (q.QuadraticInequalityLessFactory, "x^2 - x - 2 < 0",
     {"exercise": "x^2 - x - 2 < 0", "solution_range": "(-1, 2)", "parabola_up": True}),
    (q.QuadraticInequalityGreaterFactory, "x^2 - 3x + 2 > 0",
     {"exercise": "x^2 - 3x + 2 > 0", "solution_range": "(-∞, 1) U (2, ∞)", "parabola_up": True}),
])
def test_quadratic_solve(factory_class, test_input, expected_output):
    factory = factory_class()
    solution = factory.solve(test_input)

    assert solution == expected_output, f"Expected {expected_output}, but got {solution}"

