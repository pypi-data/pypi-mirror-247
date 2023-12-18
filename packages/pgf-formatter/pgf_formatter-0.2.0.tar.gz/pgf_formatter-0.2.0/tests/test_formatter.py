import matplotlib.pyplot as plt

from pgf_formatter.formatter import matplotlib_figure_to_pgf


class P:
    def __init__(self):
        self._text = ""

    def text(self, text):
        self._text = text


def test_formatter():
    fig, ax = plt.subplots(figsize=(3, 4))
    ax.plot([1, 2])
    matplotlib_figure_to_pgf(fig, p := P(), None)
    assert p._text.startswith("%% Creator: Matplotlib, PGF backend")
    assert p._text.endswith("\\endgroup%\n")
