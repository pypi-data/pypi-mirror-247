from pathlib import Path

from matplotlib import pyplot


def apply_basic_style():
    pyplot.style.use(f"{Path(__file__).parent}/basic.mplstyle")
