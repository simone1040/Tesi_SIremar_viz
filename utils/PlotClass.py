from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt
from matplotlib.figure import Figure

from controllers import CaricoManager


class PlotRunnable(QRunnable):
    def __init__(self, dialog):
        QRunnable.__init__(self)
        self.w = dialog
    def run(self):
        figure = CaricoManager.image_statistics_filtered(self.w.data)
        QMetaObject.invokeMethod(self.w, "stop_spinner",
                                 Qt.QueuedConnection,
                                 Q_ARG(Figure, figure))