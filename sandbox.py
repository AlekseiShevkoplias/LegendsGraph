import sys
import matplotlib; matplotlib.use("Qt5Agg")

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from netgraph import EditableGraph


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.graph = EditableGraph([(6, 41), (11, 26), (28, 29), (30, 10), (21, 1), (40, 15), (17, 27), (23, 10), (36, 35), (26, 12), (33, 20), (38, 21), (27, 15), (13, 18), (28, 19), (12, 4), (4, 19), (45, 16), (38, 46), (32, 13), (2, 26), (33, 9), (34, 6), (16, 48), (21, 33), (42, 48), (36, 14), (14, 12), (7, 18), (5, 39), (5, 29), (18, 47), (13, 37), (2, 6), (34, 48), (26, 6), (22, 48), (1, 6), (3, 12), (31, 21), (5, 18), (7, 15), (28, 12), (18, 25), (13, 23), (27, 35), (38, 37), (29, 31), (4, 30), (22, 21)], ax=self.ax)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Enable key_press_event events:
        # https://github.com/matplotlib/matplotlib/issues/707/#issuecomment-4181799
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)

        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()


if __name__ == "__main__":
    main()	
