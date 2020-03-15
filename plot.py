from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
from io import BytesIO


class MyFigure(Figure):
    def __init__(self, *args, figtitle='hi mom', **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        super().__init__(*args, **kwargs)
        self.text(0.5, 0.95, figtitle, ha='center')
        self.patch.set_facecolor('#191919')


def create_plot(data):
    # Generate the figure **without using pyplot**.
    plt.style.use('dark_background')
    fig = plt.figure(FigureClass=MyFigure, figtitle='my title')
    fig.patch.set_facecolor('#191919')
    ax = fig.subplots()

    ax.set_facecolor('#191919')

    ax.plot(range(data[0]), data[1])
    ax.plot(range(data[0]), data[2])
    ax.plot(range(data[0]), data[3])

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    print(fig)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64, {data}"
