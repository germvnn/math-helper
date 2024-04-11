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
        assert factory.operator_symbol.strip() in exercise

        # Check amount of components in exercise
        components = exercise.split(factory.operator_symbol)
        component_count = 3 if level > 3 else 2
        assert len(components) == component_count
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

