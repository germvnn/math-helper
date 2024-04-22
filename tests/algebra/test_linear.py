import random

import pytest

from MathGenerator.algebra.linear import (SingleLinearEquationFactory,
                                          SingleLinearInequalityLessFactory,
                                          SingleLinearInequalityGreaterFactory,
                                          SingleLinearEqualLessFactory,
                                          SingleLinearEqualGreaterFactory)


@pytest.mark.parametrize("factory, level", [
    (SingleLinearEquationFactory, 1),
    (SingleLinearInequalityLessFactory, 2),
    (SingleLinearInequalityGreaterFactory, 3),
    (SingleLinearEqualLessFactory, 4),
    (SingleLinearEqualGreaterFactory, 5),
])
def test_linear_generate(factory, level):
    factory = factory()
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)

    assert len(exercises) == amount, f"Generated {len(exercises)} exercises, expected {amount}"

    for exercise in exercises:
        assert factory.operator in exercise, f"Operator {factory.operator} not found in {exercise}"


@pytest.mark.parametrize("factory, exercises, expected", [
    (SingleLinearEquationFactory,
     ['-2x - 2 = = -3x - 1'], {'-2x - 2 = = -3x - 1': 'x = 1'}),
    (SingleLinearInequalityLessFactory,
     ['2x - 3 < 1'], {'2x - 3 < 1': 'x < 2'}),
    (SingleLinearInequalityGreaterFactory,
     ['4x + 1 > 5'], {'4x + 1 > 5': 'x > 1'}),
    (SingleLinearEqualLessFactory,
     ['x - 2 <= 2'], {'x - 2 <= 2': 'x <= 4'}),
    (SingleLinearEqualGreaterFactory,
     ['-2x + 3 >= 1'], {'-2x + 3 >= 1': 'x <= 1'})
])
def test_linear_solve(factory, exercises, expected):
    factory = factory()
    solutions = factory.solve(exercises)
    assert solutions == expected, f"Test failed for {factory.__class__.__name__}"
