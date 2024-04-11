import pytest
from MathGenerator.arithmetic.addition import AdditionFactory


@pytest.mark.parametrize("level, amount, component_count", [
    (1, 3, 2),  # Level 1 - 2 components
    (2, 4, 2),  # Level 2 - 2 components
    (3, 1, 2),  # Level 3 - 2 components
    (4, 3, 3),  # Level 4 - 3 components
    (5, 2, 3)   # Level 5 - 3 components
])
def test_addition_generate(level, amount, component_count):
    factory = AdditionFactory()
    questions = factory.generate(level, amount)

    # First, check if the amount of generated questions matches the expected amount
    assert len(questions) == amount

    for question in questions:
        components = question.split(" + ")

        # Check amount of components in exercise
        assert len(components) == component_count
        # Validate components
        assert all(component.isdigit() for component in components)
