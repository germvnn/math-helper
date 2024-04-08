import random


def create_quadratic_equation():
    a = random.randint(-3, -3)
    while a == 0:
        a = random.randint(-3, 3)

    x1 = random.randint(-10, 10)
    x2 = random.randint(-10, 10)

    # Obliczenie współczynników b i c
    b = -(x1 + x2) * a
    c = x1 * x2 * a
    a_str = f"{'-' if a == -1 else '' if a == 1 else a}"

    # Zwrócenie równania kwadratowego z uwzględnieniem specjalnego formatowania dla a
    return f"{a_str}x^2 + {b}x + {c} = 0", x1, x2


print(create_quadratic_equation())
