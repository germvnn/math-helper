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
def test_arithmetic_fraction_generate(factory, level, expected_component_amount, scaling):
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


@pytest.mark.parametrize("factory, level, expected_component_amount", [
    (f.PercentAdditionFactory(), 5, 3),
    (f.PercentAdditionFactory(), 3, 2),
    (f.PercentSubtractionFactory(), 3, 2),
    (f.PercentSubtractionFactory(), 6, 3),
    (f.PercentMultiplicationFactory(), 5, 3),
    (f.PercentMultiplicationFactory(), 3, 2)
])
def test_arithmetic_percent_generate(factory, level, expected_component_amount):
    amount = random.randint(1, 10)
    exercises = factory.generate(level=level, amount=amount)
    max_number = 100

    assert len(exercises) == amount,\
        f"Number of exercises {len(exercises)}, Expected: {amount}"

    for exercise in exercises:
        assert factory.operator_symbol.strip() in exercise, \
            f"There are no expected operator: {factory.operator_symbol.strip()}"
        components = exercise.split(factory.operator_symbol)
        assert len(components) == expected_component_amount, \
            f"Number of components: {len(components)}, Expected: {expected_component_amount}"
        for component in components:
            # Validate that percentage is in component
            assert '%' in component, f"There are no % in {component}"
            assert float(component.strip('%')) < max_number, \
                f"Component {component} > {max_number}"


@pytest.mark.parametrize("factory, exercises_results", [
    (f.AdditionFactory(),
     {'7712 + 2211 + 2458': 12381, '9209 + 5627 + 16': 14852}),
    (f.SubtractionFactory(),
     {'58 - 1': 57, '33 - 11': 22, '75 - 64': 11, '62 - 32': 30, '47 - 22': 25}),
    (f.MultiplicationFactory(),
     {'94 * 742': 69748, '5 * 589': 2945, '314 * 6': 1884}),
    (f.DivisionFactory(),
     {'256 / 16': 16, '1000 / 10': 100, '333 / 111': 3}),
    (f.FractionAdditionFactory(),
     {'6.91 + 1.95': 8.86, '7.21 + 2.2': 9.41, '0.92 + 3.21': 4.13}),
    (f.FractionSubtractionFactory(),
     {'14.5 - 11.12': 3.38, '57.82 - 34.5': 23.32, '51.78 - 65.06': -13.28}),
    (f.FractionMultiplicationFactory(),
     {'6.7 * 49.4': 330.98, '69.6 * 34.2': 2380.32, '10.3 * 99.7': 1026.91}),
    (f.FractionDivisionFactory(),
     {'182.4 / 4.3': 42.419, '663.9 / 7.4': 89.716, '275.8 / 8.8': 31.341}),
    (f.PercentAdditionFactory(),
     {
         '87.8% + 45.0%': '132.8%',
         '68.87% + 44.0618%': '112.9318%',
         '44.0% + 39.72%': '83.72%',
         '53.9% + 19.4%': '73.3%',
         '34.065% + 75.03%': '109.095%'
     }),
    (f.PercentSubtractionFactory(),
     {
         '38.3171% - 82.317%': '-43.9999%',
         '91.0% - 85.748%': '5.252%',
         '58.5% - 83.5068%': '-25.0068%',
         '84.04% - 27.6%': '56.44%',
         '46.1582% - 83.2097%': '-37.0515%'
     }),
    (f.PercentMultiplicationFactory(),
     {
         '50% * 50%': '25.0%',
         '100% * 75%': '75.0%',
         '25% * 50%': '12.5%',
         '5.66% * 39.9%': '2.2583%',
         '53.45% * 34.05%': '18.1997%'
     })
])
def test_arithmetic_solve(factory, exercises_results):
    for exercise, expected_result in exercises_results.items():
        result = factory.solve([exercise])[exercise]
        assert result == expected_result, f"Failed at {exercise}: got {result}, expected {expected_result}"

