import glob
import os
import re

import numpy as np
import matplotlib.pyplot as plt
from pylatex import NoEscape


def latexify(text):
    """Escape LaTeX special characters in a given text."""
    # TODO: Implement functionality for the rest special characters
    if isinstance(text, (int, float)):
        return text
    return text.replace('%', '\\%')


def exercise_string(numerator, exercise, end_line):
    exercise = exercise.replace('<=', r'\leq')
    exercise = exercise.replace('>=', r'\geq')
    return NoEscape(rf"{numerator}.~~~$${latexify(exercise)}$$ {end_line}")


def solution_string(numerator, exercise, comparison_operator, solution):
    return NoEscape(rf"{numerator}.~~~$${latexify(exercise)}$$ {comparison_operator} {latexify(solution)}")


def quadratic_solution_string(roots, delta):
    if isinstance(roots, tuple):
        if len(roots) == 1:
            solution_text = rf"x_1 = x_2 = {roots[0]}, ~~~~ \Delta = {delta}"
        elif len(roots) == 2:
            solution_text = rf"x_1 = {roots[0]}, ~~~~ x_2 = {roots[1]}, ~~~~ \Delta = {delta}"
        else:
            solution_text = "WRONG FORMAT"
    else:
        solution_text = "No~real~roots,~complex~roots~present,~" + rf"~~~~ \Delta = {delta}"
    return NoEscape(r'\begin{center}\Large $' + solution_text + r'$ \end{center}')


def extract_quadratic_coefficients(exercise: str):
    # Normalize exercise
    exercise = re.split('=|<|>|<=|>=', exercise.replace(' ', ''))[0]
    # Extraction coefficients a, b, c
    coeffs = re.findall(r'([+-]?\d*\.?\d*)x\^2|([+-]?\d*\.?\d*)x|([+-]?\d+)', exercise)
    a = int(coeffs[0][0] if coeffs[0][0] != '' and coeffs[0][0] != '+' and coeffs[0][0] != '-' else (
        '1' if coeffs[0][0] == '' or coeffs[0][0] == '+' else '-1'))
    b = int(coeffs[1][1] if coeffs[1][1] != '' and coeffs[1][1] != '+' and coeffs[1][1] != '-' else (
        '1' if coeffs[1][1] == '' or coeffs[1][1] == '+' else '-1'))
    c = int(coeffs[2][2] if coeffs[2][2] else 0)
    return a, b, c


def plot_quadratic(numerator: int, exercise: str, solution: dict):
    roots = solution['roots']
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
    plt.savefig(os.path.join(os.path.dirname(__file__), f'plot{numerator}.png'))


def remove_plots():
    files_to_remove = glob.glob(os.path.join(os.path.dirname(__file__), 'plot*'))

    for file_path in files_to_remove:
        os.remove(file_path)
