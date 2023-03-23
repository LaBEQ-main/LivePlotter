# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Authors - Frank Duffy, LaBEQ / Sardashti Research Group, Clemson University
#
# Based on tutorials about matplotlib animate by Corey Schafer and multiprocessing
# by Engineer Man
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------

import enaml
from enaml.qt.qt_application import QtApplication

from liveplotter_driver import LivePlotter


if __name__ == '__main__':
    with enaml.imports():
        from liveplotter_view import Main

    liveplot = LivePlotter()

    app = QtApplication()

    view = Main(plotter=liveplot)
    # view = LivePlotterView()
    view.show()

    app.start()