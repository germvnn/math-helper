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
        solution_text = "No real roots, complex roots present, " + rf"~~~~ \Delta = {delta}"
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
    x_range = max(roots) - min(roots)
    x = np.linspace(min(roots) - 0.5 * x_range, max(roots) + 0.5 * x_range, 400)
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
    fill_kwargs = {'color': 'gray', 'alpha': 0.7, 'hatch': '//'}

    # Scatter settings
    scatter_kwargs = {'zorder': 5, 's': 35, 'edgecolors': 'red', 'linewidths': 1.5}

    # Check for inequality and apply the appropriate fill and scatter properties
    if '=' in exercise and '<' not in exercise and '>' not in exercise:
        plt.scatter(roots, [0, 0], facecolors='red', **scatter_kwargs)
    elif '<=' in exercise:
        plt.fill_between(x, y, 0, where=(y <= 0), **fill_kwargs)
        plt.scatter(roots, [0, 0], facecolors='red', **scatter_kwargs)
    elif '>=' in exercise:
        plt.fill_between(x, y, 0, where=(y >= 0), **fill_kwargs)
        plt.scatter(roots, [0, 0], facecolors='red', **scatter_kwargs)
    elif '<' in exercise:
        plt.fill_between(x, y, 0, where=(y < 0), **fill_kwargs)
        plt.scatter(roots, [0, 0], facecolors='none', **scatter_kwargs)
    else:  # For '>'
        plt.fill_between(x, y, 0, where=(y > 0), **fill_kwargs)
        plt.scatter(roots, [0, 0], facecolors='none', **scatter_kwargs)

    plt.legend()
    plt.savefig(os.path.join(os.path.dirname(__file__), f'plot{numerator}.png'))


def remove_plots():
    files_to_remove = glob.glob(os.path.join(os.path.dirname(__file__), 'plot*'))

    for file_path in files_to_remove:
        os.remove(file_path)
