import logging
import pytest
import random
from MathGenerator.arithmetic.factories import (AdditionFactory,
                                                SubtractionFactory,
                                                MultiplicationFactory,
                                                DivisionFactory)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("factory, level, expected_component_amount", [
    (AdditionFactory(), 5, 3),
    (AdditionFactory(), 3, 2),
    (SubtractionFactory(), 6, 3),
    (SubtractionFactory(), 3, 2),
    (MultiplicationFactory(), 3, 2),
    (MultiplicationFactory(), 5, 3),
    # Always 2 components expected in division
    (DivisionFactory(), 3, 2),
    (DivisionFactory(), 4, 2),
    (DivisionFactory(), 5, 2),
])
def test_arithmetic_generate(factory, level, expected_component_amount):
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)

    # First, check if the amount of generated exercises matches the expected amount
    assert len(exercises) == amount

    for exercise in exercises:

        # Validate operator
        assert factory.operator_symbol.strip() in exercise

        # Check amount of components in exercise
        components = exercise.split(factory.operator_symbol)
        assert len(components) == expected_component_amount

        # Validate components
        assert all(component.isdigit() for component in components)


@pytest.mark.parametrize("factory, exercises, expected_results", [
    (AdditionFactory(), ['7712 + 2211 + 2458', '9209 + 5627 + 16'], [12381, 14852]),
    (SubtractionFactory(), ['58 - 1', '33 - 11', '75 - 64', '62 - 32', '47 - 22'], [57, 22, 11, 30, 25]),
    (MultiplicationFactory(), ['94 * 742', '5 * 589', '314 * 6'], [69748, 2945, 1884]),
    (DivisionFactory(), ['256 / 16', '1000 / 10', '333 / 111'], [16, 100, 3])
])
def test_arithmetic_solve(factory, exercises, expected_results):
    assert factory.solve(exercises) == expected_results
