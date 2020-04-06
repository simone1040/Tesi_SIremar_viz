from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt
from matplotlib.figure import Figure

from controllers import CaricoManager


class PlotRunnable(QRunnable):
    def __init__(self, dialog):
        QRunnable.__init__(self)
        self.w = dialog

    def run(self):
        figure = CaricoManager.image_statistics_filtered(self.w.data)
        if figure:
            QMetaObject.invokeMethod(self.w, "set_image_carico",
                                 Qt.QueuedConnection,
                                 Q_ARG(Figure, figure))
        else:
            QMetaObject.invokeMethod(self.w, "error_cargo_not_found",
                                     Qt.QueuedConnection,
                                     Q_ARG(str, "Nessun carico trovato nella range di data selezionato. Riprova con un range diverso"))