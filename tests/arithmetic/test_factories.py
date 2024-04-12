import logging
import pytest
import random
from MathGenerator.arithmetic import factories as f

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("factory, level, expected_component_amount", [
    (f.AdditionFactory(), 5, 3),
    (f.AdditionFactory(), 3, 2),
    (f.SubtractionFactory(), 6, 3),
    (f.SubtractionFactory(), 3, 2),
    (f.MultiplicationFactory(), 3, 2),
    (f.MultiplicationFactory(), 5, 3),
    # Always 2 components expected in division
    (f.DivisionFactory(), 3, 2),
    (f.DivisionFactory(), 4, 2),
    (f.DivisionFactory(), 5, 2),
])
def test_arithmetic_generate(factory, level, expected_component_amount):
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)
    max_number = 10 ** level if not isinstance(factory, f.MultiplicationFactory) else (10 ** level) / 5 + 10

    # First, check if the amount of generated exercises matches the expected amount
    assert len(exercises) == amount, \
        f"Number of exercises {len(exercises)}, Expected: {amount}"

    for exercise in exercises:

        # Validate operator
        assert factory.operator_symbol.strip() in exercise, \
            f"There are no expected operator: {factory.operator_symbol.strip()}"

        # Check amount of components in exercise
        components = exercise.split(factory.operator_symbol)
        assert len(components) == expected_component_amount, \
            f"Number of components: {len(components)}, Expected: {expected_component_amount}"

        # Validate components
        for component in components:
            assert component.isdigit(), f"Component {component} contains non-digit value"
            assert int(component) <= max_number, f"Component {component} > {max_number}"


@pytest.mark.parametrize("factory, level, expected_component_amount, scaling", [
    (f.FractionAdditionFactory(), 5, 3, False),
    (f.FractionSubtractionFactory(), 3, 2, False),
    (f.FractionMultiplicationFactory(), 5, 3, True),
    (f.FractionDivisionFactory(), 4, 2, True),
    (f.FractionDivisionFactory(), 5, 2, True),
])
def test_fraction_arithmetic_generate(factory, level, expected_component_amount, scaling):
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)
    divisor = 10 if scaling else 100
    max_number = (10 ** level) / divisor

    assert len(exercises) == amount,\
        f"Number of exercises {len(exercises)}, Expected: {amount}"

    for exercise in exercises:
        assert factory.operator_symbol.strip() in exercise, \
            f"There are no expected operator: {factory.operator_symbol.strip()}"
        components = exercise.split(factory.operator_symbol)
        assert len(components) == expected_component_amount, \
            f"Number of components: {len(components)}, Expected: {expected_component_amount}"
        for component in components:
            assert component.replace('.', '', 1).isdigit(), \
                f"Component {component} is not a valid number"
            assert float(component) < max_number, \
                f"Component {component} > {max_number}"


@pytest.mark.parametrize("factory, exercises, expected_results", [
    (f.AdditionFactory(), ['7712 + 2211 + 2458', '9209 + 5627 + 16'], [12381, 14852]),
    (f.SubtractionFactory(), ['58 - 1', '33 - 11', '75 - 64', '62 - 32', '47 - 22'], [57, 22, 11, 30, 25]),
    (f.MultiplicationFactory(), ['94 * 742', '5 * 589', '314 * 6'], [69748, 2945, 1884]),
    (f.DivisionFactory(), ['256 / 16', '1000 / 10', '333 / 111'], [16, 100, 3]),
    (f.FractionAdditionFactory(), ['6.91 + 1.95', '7.21 + 2.2', '0.92 + 3.21'], [8.86, 9.41, 4.13]),
    (f.FractionSubtractionFactory(), ['14.5 - 11.12', '57.82 - 34.5', '51.78 - 65.06'], [3.38, 23.32, -13.28]),
    (f.FractionMultiplicationFactory(), ['6.7 * 49.4', '69.6 * 34.2', '10.3 * 99.7'], [330.98, 2380.32, 1026.91]),
    (f.FractionDivisionFactory(), ['182.4 / 4.3', '663.9 / 7.4', '275.8 / 8.8'], [42.419, 89.716, 31.341]),
])
def test_arithmetic_solve(factory, exercises, expected_results):
    assert factory.solve(exercises) == expected_results, f"Expected results: {expected_results}"
