from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
from io import BytesIO


class MyFigure(Figure):
    def __init__(self, *args, figtitle='hi mom', **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        super().__init__(*args, **kwargs)
        self.text(0.5, 0.95, figtitle, ha='center')


def create_plot(data):
    plt.rcParams['lines.linewidth'] = 3
    plt.rcParams['axes.facecolor'] = '#191919'
    plt.rcParams['savefig.facecolor'] = '#191919'
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['patch.edgecolor'] = 'white'
    plt.rcParams['hatch.color'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['axes.titlecolor'] = 'white'
    fig = plt.figure(FigureClass=MyFigure, figtitle='')
    ax = fig.subplots()

    ax.plot(range(data[0]), data[1], c='#e15000')
    ax.plot(range(data[0]), data[2], c='r')
    ax.plot(range(data[0]), data[3], c='g')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    print(fig)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64, {data}"
