import random

import pytest

from MathGenerator.algebra.quadratic import *


@pytest.mark.parametrize("factory_class, level", [
    (QuadraticEquationFactory, 2),
    (QuadraticInequalityLessFactory, 2),
    (QuadraticInequalityGreaterFactory, 2),
])
def test_quadratic_generate(factory_class, level):
    factory = factory_class()
    amount = random.randint(1, 10)  # Generate a random number of exercises to create
    exercises = factory.generate(level=level, amount=amount)

    assert len(exercises) == amount, f"Generated {len(exercises)} exercises, expected {amount}"

    for exercise in exercises:
        assert factory.operator_symbol in exercise, f"Operator {factory.operator_symbol} not found in {exercise}"

        if level > 3:
            assert 'sqrt' in exercise
        # Assuming the quadratic exercise is structured like 'ax^2 + bx + c operator 0'
        components = exercise.replace(" ", "").split(factory.operator_symbol)

        assert components[1] is '0'
        left_side = components[0]  # Only one side as the other is assumed to be '0'

        # Check components of the quadratic expression
        assert left_side.count('x^2') == 1 and left_side.count('x') == 1, "Malformed quadratic expression"


@pytest.mark.parametrize("factory_class, test_input, expected_output", [
    (QuadraticEquationFactory, "x^2 - 5x + 6 = 0",
     {"exercise": "x^2 - 5x + 6 = 0", "x1": 2, "x2": 3, "parabola_up": True}),
    (QuadraticInequalityLessFactory, "x^2 - x - 2 < 0",
     {"exercise": "x^2 - x - 2 < 0", "solution_range": "(-1, 2)", "parabola_up": True}),
    (QuadraticInequalityGreaterFactory, "x^2 - 3x + 2 > 0",
     {"exercise": "x^2 - 3x + 2 > 0", "solution_range": "(-∞, 1) U (2, ∞)", "parabola_up": True}),
])
def test_quadratic_solve(factory_class, test_input, expected_output):
    factory = factory_class()
    solution = factory.solve(test_input)

    assert solution == expected_output, f"Expected {expected_output}, but got {solution}"

