import matplotlib.ticker as ptick
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

from .config import AxConfig, SpineConfig


def apply_x_config(ax: Axes, config: SpineConfig = SpineConfig()):
    ax.set_xlabel(config.label)

    if config.scale == "log":
        ax.set_xscale("log", base=10)

    if config.scale == "linear":
        if config.step is not None:
            ax.xaxis.set_major_locator(ptick.MultipleLocator(config.step))
        ax.xaxis.set_major_formatter(FixedOrderFormatter(0, useMathText=True))
        if config.pow != 0:
            ax.ticklabel_format(
                style="sci", axis="x", scilimits=(config.pow, config.pow)
            )

    if config.lim is not None:
        ax.set_xlim(config.lim)
    else:
        ax.set_xlim(0, ax.get_xlim()[1])

    if not config.visible:
        ax.xaxis.set_ticks([])

    if config.invert:
        ax.invert_xaxis()


def apply_y_config(ax: Axes, config: SpineConfig = SpineConfig()):
    ax.set_ylabel(config.label)

    if config.scale == "log":
        ax.set_yscale("log", base=10)

    if config.scale == "linear":
        if config.step is not None:
            ax.yaxis.set_major_locator(ptick.MultipleLocator(config.step))
        ax.yaxis.set_major_formatter(FixedOrderFormatter(0, useMathText=True))
        if config.pow != 0:
            ax.ticklabel_format(
                style="sci", axis="y", scilimits=(config.pow, config.pow)
            )

    if config.lim is not None:
        ax.set_ylim(config.lim)
    else:
        ax.set_ylim(0, ax.get_ylim()[1])

    if not config.visible:
        ax.yaxis.set_ticks([])

    if config.invert:
        ax.invert_yaxis()


def apply_ax_config(ax: Axes, config: AxConfig = AxConfig()):
    apply_x_config(ax, config.x)
    apply_y_config(ax, config.y)
    ax.legend(loc=config.legends_loc)
    if config.bbox_to_anchor is not None:
        ax.legend(loc=config.legends_loc, bbox_to_anchor=config.bbox_to_anchor)


class FixedOrderFormatter(ScalarFormatter):
    def __init__(self, order_of_mag=0, useOffset=True, useMathText=True):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(
            self,
            useOffset=useOffset,
            useMathText=useMathText,
        )

    def _set_orderOfMagnitude(self, range):
        self.orderOfMagnitude = self._order_of_mag
