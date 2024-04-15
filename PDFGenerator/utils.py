from pylatex import NoEscape


def latexify(text):
    """Escape LaTeX special characters in a given text."""
    # TODO: Implement functionality for the rest special characters
    if isinstance(text, (int, float)):
        return text
    return text.replace('%', '\\%')


def exercise_string(numerator, exercise, end_line):
    return NoEscape(rf"{numerator}.~~~{latexify(exercise)} {end_line}")


def solution_string(numerator, exercise, comparison_operator, solution):
    return NoEscape(rf"{numerator}.~~~{latexify(exercise)} {comparison_operator} {latexify(solution)}")
