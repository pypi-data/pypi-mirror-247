import math

from matplotlib import pyplot as plt

from .style.apply import apply_basic_style


def calc_grid(number_of_subplots: int):
    return math.ceil(math.sqrt(number_of_subplots))


def make_graph(
    number_of_subplots: int = 1, row: int | None = None, column: int | None = None
):
    fig = plt.figure()
    grid = calc_grid(number_of_subplots)
    row = row or grid
    column = column or grid
    axes = [fig.add_subplot(row, column, i + 1) for i in range(number_of_subplots)]
    apply_basic_style()
    return fig, axes
