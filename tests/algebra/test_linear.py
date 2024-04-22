import random

import pytest

from MathGenerator.algebra import linear as l


@pytest.mark.parametrize("factory_class, level", [
    (l.SingleLinearEquationFactory, 1),
    (l.SingleLinearInequalityLessFactory, 2),
    (l.SingleLinearInequalityGreaterFactory, 3),
    (l.SingleLinearEqualLessFactory, 4),
    (l.SingleLinearEqualGreaterFactory, 5),
])
def test_linear_generate(factory_class, level):
    factory = factory_class()
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)

    assert len(exercises) == amount, f"Generated {len(exercises)} exercises, expected {amount}"

    for exercise in exercises:
        assert factory.operator in exercise, f"Operator {factory.operator} not found in {exercise}"
