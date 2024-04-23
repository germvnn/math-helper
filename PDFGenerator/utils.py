from fractions import Fraction
import glob
import os
import re

import numpy as np
import matplotlib.pyplot as plt
from pylatex import NoEscape


def decimal_to_fraction(expression):
    # Look for decimal parts in expression
    decimals = re.findall(r"[-+]?[0-9]*\.?[0-9]+", expression)
    # Convert every decimal part into fraction
    for dec in decimals:
        fraction = Fraction(float(dec)).limit_denominator()
        # Round expression if fraction too complicated
        if len(str(fraction.denominator)) > 3:
            # TODO: Implement \\approx somehow
            expression = expression.replace(dec, str(round(float(dec), 4)))
            continue
        expression = expression.replace(dec, str(fraction))
    # Convert every decimal parts to LaTeX formatted fractions
    fractions = re.findall(r"(\d+)/(\d+)", expression)
    for num, den in fractions:
        expression = expression.replace(f"{num}/{den}", f"\\frac{{{num}}}{{{den}}}")
    return expression


def extract_quadratic_coefficients(exercise: str):
    # Normalize exercise
    exercise = re.split('=|<|>|<=|>=', exercise.replace(' ', ''))[0]
    # Extraction coefficients a, b, c
    coeffs = re.findall(r'(-?\d*\.?\d*)x\^2|(-?\d*\.?\d*)x|(-?\d*\.?\d+)', exercise)
    a = int(coeffs[0][0] if coeffs[0][0] != '' and coeffs[0][0] != '+' and coeffs[0][0] != '-' else (
        '1' if coeffs[0][0] == '' or coeffs[0][0] == '+' else '-1'))
    b = int(coeffs[1][1] if coeffs[1][1] != '' and coeffs[1][1] != '+' and coeffs[1][1] != '-' else (
        '1' if coeffs[1][1] == '' or coeffs[1][1] == '+' else '-1'))
    c = float(coeffs[2][2] if coeffs[2][2] else 0)
    return a, b, c


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


def linear_exercise_string(numerator, exercise):
    exercise = exercise.replace('<=', r'\leq')
    exercise = exercise.replace('>=', r'\geq')
    return NoEscape(rf"{numerator}.~~~$${latexify(decimal_to_fraction(exercise))}$$")


def quadratic_exercise_string(numerator, exercise):
    exercise = exercise.replace('<=', r'\leq')
    exercise = exercise.replace('>=', r'\geq')
    # TODO: Temporary solution. Parentheses must be implemented in generator
    a, b, c = extract_quadratic_coefficients(exercise)
    for coeff in [b, c]:
        exercise = exercise.replace(str(coeff), f"({coeff})") if coeff < 0 else exercise
    return NoEscape(rf"{numerator}.~~~$${latexify(decimal_to_fraction(exercise))}$$")


def quadratic_solution_string(roots, delta):
    if isinstance(roots, tuple):
        if len(roots) == 1:
            solution_text = rf"x_1 = x_2 = {decimal_to_fraction(str(roots[0]))}, ~~~~ \Delta = {delta}"
        elif len(roots) == 2:
            solution_text = rf"x_1 = {decimal_to_fraction(str(roots[0]))},\
             ~~~~ x_2 = {decimal_to_fraction(str(roots[1]))}, ~~~~ \Delta = {delta}"
        else:
            solution_text = "WRONG FORMAT"
    else:
        solution_text = "No~real~roots,~complex~roots~present,~" + rf"~~~~ \Delta = {delta}"
    return NoEscape(r'\begin{center}\Large $' + solution_text + r'$ \end{center}')


class Plot:

    @staticmethod
    def path(numerator):
        return os.path.join(os.path.dirname(__file__), f'plot{numerator}.png')

    @staticmethod
    def linear(numerator: int, solution: str) -> bool:
        # Rozpoznaj wartość x i operator z rozwiązania
        match = re.match(r"x\s*([<>=]+)\s*([-+]?[\d.]+)", solution)
        if match:
            operator = match.group(1)
            x_value = float(match.group(2))
        else:
            return False

        plt.figure(figsize=(6, 1))
        ax = plt.gca()

        # Adjust the limits and remove y-axis
        plt.xlim(x_value - 5, x_value + 5)
        plt.ylim(-1, 1)  # Seems to be useless, but arrows stops working without it
        ax.axes.yaxis.set_visible(False)

        # Draw a line for the x-axis
        plt.axhline(0, color='black', lw=1)

        scatter_kwargs = {
            'x': x_value,
            'y': 0,
            's': 75,  # size of the marker
            'edgecolors': 'red',
            'facecolor': 'red' if '=' in solution else None,
            'linewidths': 1.5,
            'marker': 'o',
        }
        plt.scatter(**scatter_kwargs)  # Red circle no fill

        arrow_kwargs = {'linewidth': 2.5, 'head_width': 0.25, 'head_length': 0.5, 'fc': 'blue', 'ec': 'blue'}
        # Add arrows indicating the inequality
        if '>' in operator:
            plt.arrow(x_value + 0.17, 0, 4, 0, **arrow_kwargs)
        if '<' in operator:
            plt.arrow(x_value - 0.13, 0, -4, 0, **arrow_kwargs)
        plt.xlabel('x')
        plt.grid(False)
        plt.savefig(Plot.path(numerator=numerator))
        return True

    @staticmethod
    def quadratic(numerator: int, exercise: str, solution: dict):
        a, b, c = extract_quadratic_coefficients(exercise)

        # Define the quadratic function
        def f(x):
            return a * x ** 2 + b * x + c

        # Determine the x range for plotting
        if isinstance(solution['roots'], tuple):
            # If roots exist, use them to determine the x range for plotting
            x_range = max(solution['roots']) - min(solution['roots'])
            x_range = x_range if x_range != 0 else 2
            x = np.linspace(min(solution['roots']) - 0.5 * x_range, max(solution['roots']) + 0.5 * x_range, 400)
        else:
            # If no real roots, use a default range centered at the vertex
            vertex_x = -b / (2 * a)
            x = np.linspace(vertex_x - 2, vertex_x + 2, 400)
        y = f(x)

        # Generate the plot
        plt.figure(figsize=(4, 3))
        plt.plot(x, y, label=f'y = {a:.1f}x^2 + {b:.1f}x + {c:.1f}', lw=2.5, color='blue')
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(False)

        # Fill settings
        fill = (y > 0) if '>' in exercise else ((y < 0) if '<' in exercise else None)
        fill_kwargs = {'where': fill, 'color': 'gray', 'alpha': 0.7, 'hatch': '//'}

        # Scatter settings
        color = 'red' if '=' in exercise else None  # = indicates that scatter must be filled
        scatter_kwargs = {'facecolors': color, 'zorder': 5, 's': 35, 'edgecolors': 'red', 'linewidths': 1.5}

        # Check for delta and apply the appropriate fill and scatter properties
        if solution['delta'] > 0:
            # When delta is positive, plot the roots
            plt.scatter(solution['roots'], [0, 0], **scatter_kwargs)
            if fill is not None:
                plt.fill_between(x, y, 0, **fill_kwargs)
        elif solution['delta'] == 0:
            # When delta is zero, plot the single root
            plt.scatter(solution['roots'], [0], **scatter_kwargs)
            if fill is not None:
                plt.fill_between(x, y, 0, **fill_kwargs)
        else:
            # When delta is negative, no real roots to plot, but the parabola still needs to be shown
            if fill is not None:
                plt.fill_between(x, y, 0, **fill_kwargs)

        plt.legend()
        plt.savefig(Plot.path(numerator=numerator))

    @staticmethod
    def remove():
        files_to_remove = glob.glob(os.path.join(os.path.dirname(__file__), 'plot*'))

        for file_path in files_to_remove:
            os.remove(file_path)
