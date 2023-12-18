import io
import sys

from IPython.core.getipython import get_ipython
from matplotlib import rcParams
from matplotlib.figure import Figure
from matplotlib_inline.backend_inline import set_matplotlib_formats


def set_params(mathfont="stix", dpi=200):
    set_matplotlib_formats("retina")
    if sys.platform.startswith("win"):
        rcParams["font.sans-serif"] = ["Meiryo", "DejaVu Sans"]
        rcParams["font.serif"] = ["Meiryo", "DejaVu Sans"]
    rcParams["figure.dpi"] = dpi
    rcParams["font.family"] = "serif"
    rcParams["mathtext.fontset"] = mathfont
    rcParams["ytick.alignment"] = "center"


def matplotlib_figure_to_pgf(fig: Figure, p, cycle):
    with io.StringIO() as fp:
        try:
            fig.savefig(fp, format="pgf", bbox_inches="tight")
        except ValueError:
            text = "Figure"
        else:
            text = fp.getvalue()
    p.text(text)


def set_formatter():
    if ip := get_ipython():
        formatter = ip.display_formatter.formatters["text/plain"]  # type:ignore
        formatter.for_type(Figure, matplotlib_figure_to_pgf)
