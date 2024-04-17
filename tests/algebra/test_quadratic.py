import pytest
import random
import re

from MathGenerator.algebra import quadratic as q


@pytest.mark.parametrize("factory_class, level", [
    (q.QuadraticEquationFactory, 2),
    (q.QuadraticInequalityLessFactory, 2),
    (q.QuadraticInequalityGreaterFactory, 2),
    (q.QuadraticEqualLessFactory, 2),
    (q.QuadraticEqualGreaterFactory, 2)
])
def test_quadratic_generate(factory_class, level):
    factory = factory_class()
    amount = random.randint(1, 10)  # Generate a random number of exercises to create
    exercises = factory.generate(level=level, amount=amount)

    assert len(exercises) == amount, f"Generated {len(exercises)} exercises, expected {amount}"

    for exercise in exercises:
        assert factory.operator_symbol in exercise, f"Operator {factory.operator_symbol} not found in {exercise}"

        # Assuming the quadratic exercise is structured like 'ax^2 + bx + c operator 0'
        components = exercise.split(f" {factory.operator_symbol} ")

        assert components[1] is '0'
        left_side = components[0]  # Only one side as the other is assumed to be '0'

        # Count all occurrences of x
        all_x = re.findall(r'x', left_side)
        # Count only x^2
        x_squared = re.findall(r'x\^2', left_side)

        assert len(x_squared) == 1, "Should be exactly one 'x^2' term."
        # Since each x^2 includes two x's, adjust the count of single x's
        assert len(all_x) - len(x_squared) == 1, "Should be exactly one 'x'"


equations_list = [
    'x^2 - 2x + 1 = 0',
    'x^2 - 4x + 4 = 0',
    'x^2 + 4x + 5 = 0',
    '-2x^2 + 10x + -8 = 0',
    'x^2 + x - 6 = 0'
]


@pytest.mark.parametrize("factory, exercises, expected", [
    (q.QuadraticEquationFactory, ['x^2 - 2x + 1 = 0'],
     {'x^2 - 2x + 1 = 0': {"roots": (1,), "parabola_direction": "up", "delta": 0}}),
    (q.QuadraticEquationFactory, ['x^2 + 4x + 5 = 0', '-2x^2 + 10x + -8 = 0'],
     {
         'x^2 + 4x + 5 = 0': {"roots": "No real roots, complex roots present", "parabola_direction": "up", "delta": -4},
         '-2x^2 + 10x + -8 = 0': {"roots": (1, 4), "parabola_direction": "down", "delta": 36}
      }),
    (q.QuadraticInequalityLessFactory, ['x^2 + x - 6 < 0'],
     {'x^2 + x - 6 < 0': {"roots": (2, -3), "parabola_direction": "up", "delta": 25}}),
    (q.QuadraticInequalityGreaterFactory, ['-x^2 + 4x - 3 > 0'],
     {'-x^2 + 4x - 3 > 0': {"roots": (1, 3), "parabola_direction": "down", "delta": 4}}),
    (q.QuadraticEqualLessFactory, ['x^2 + x - 6 <= 0'],
     {'x^2 + x - 6 <= 0': {"roots": (2, -3), "parabola_direction": "up", "delta": 25}}),
    (q.QuadraticEqualGreaterFactory, ['-x^2 + 4x - 3 >= 0'],
     {'-x^2 + 4x - 3 >= 0': {"roots": (1, 3), "parabola_direction": "down", "delta": 4}})
])
def test_quadratic_solve(factory, exercises, expected):
    factory = factory()
    results = factory.solve(exercises)
    for equation in exercises:
        assert results[equation] == expected[equation], f"Failed for equation: {equation}"
