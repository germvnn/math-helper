import pytest
import random
from MathGenerator.arithmetic.factories import (AdditionFactory,
                                                SubtractionFactory,
                                                MultiplicationFactory,
                                                DivisionFactory)


@pytest.mark.parametrize("factory", [
    (AdditionFactory()),
    (SubtractionFactory()),
    (MultiplicationFactory()),
    (DivisionFactory())
])
def test_arithmetic_generate(factory):
    level = random.randint(1,5)
    amount = random.randint(1,10)
    exercises = factory.generate(level, amount)

    # First, check if the amount of generated exercises matches the expected amount
    assert len(exercises) == amount

    #
    for exercise in exercises:
        # Validate operator
        assert factory.operator.strip() in exercise

        # Check amount of components in exercise
        components = exercise.split(factory.operator)
        component_count = 3 if level > 3 else 2
        assert len(components) == component_count
        # Validate components
        assert all(component.isdigit() for component in components)
