# main.py
import enaml
from enaml.qt.qt_application import QtApplication

from LivePlotterOverlay import LivePlotter


if __name__ == '__main__':
    with enaml.imports():
        from liveplotter_view import Main

    liveplot = LivePlotter()

    app = QtApplication()

    view = Main(plotter=liveplot)
    # view = LivePlotterView()
    view.show()

    app.start()