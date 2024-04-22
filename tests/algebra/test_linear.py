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
     ['x - 3 = 2x - 8'], {'x - 3 = 2x - 8': 'x = 5.0'}),
    (SingleLinearInequalityLessFactory,
     ['-x + 4 < 8'], {'-x + 4 < 8': 'x > -4.0'}),
    (SingleLinearInequalityGreaterFactory,
     ['5x - 10 > 3x + 4'], {'5x - 10 > 3x + 4': 'x > 7.0'}),
    (SingleLinearEqualLessFactory,
     ['3x + 6 <= 9'], {'3x + 6 <= 9': 'x <= 1.0'}),
    (SingleLinearEqualGreaterFactory,
     ['-3x - 3 >= -6'], {'-3x - 3 >= -6': 'x <= 1.0'}),
    (SingleLinearEquationFactory,
     ['x + 2 = 2x - 5'], {'x + 2 = 2x - 5': 'x = 7.0'}),
    (SingleLinearInequalityLessFactory,
     ['2x - 4 < 6'], {'2x - 4 < 6': 'x < 5.0'}),
    (SingleLinearInequalityGreaterFactory,
     ['-3x + 1 > 4'], {'-3x + 1 > 4': 'x < -1.0'}),
    (SingleLinearEqualLessFactory,
     ['5x - 10 <= 15'], {'5x - 10 <= 15': 'x <= 5.0'}),
    (SingleLinearEqualGreaterFactory,
     ['10x + 20 >= 40'], {'10x + 20 >= 40': 'x >= 2.0'}),
    (SingleLinearEquationFactory,
     ['-5x + 5 = 0'], {'-5x + 5 = 0': 'x = 1.0'}),
    (SingleLinearInequalityLessFactory,
     ['x - 5 < 10'], {'x - 5 < 10': 'x < 15.0'}),
    (SingleLinearInequalityGreaterFactory,
     ['7x - 14 > 7'], {'7x - 14 > 7': 'x > 3.0'}),
    (SingleLinearEqualLessFactory,
     ['-x - 2 <= -1'], {'-x - 2 <= -1': 'x >= -1.0'}),
    (SingleLinearEqualGreaterFactory,
     ['10x - 20 >= 8x'], {'10x - 20 >= 8x': 'x >= 10.0'}),
])
def test_linear_solve(factory, exercises, expected):
    factory = factory()
    solutions = factory.solve(exercises)
    assert solutions == expected, f"Test failed for {factory.__class__.__name__}"
