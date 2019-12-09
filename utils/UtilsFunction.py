from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from utils.Costants import IMAGE_HEIGHT,IMAGE_WIDTH
from PyQt5.QtGui import QImage, QPixmap

def FigureToQPixmap(fig):
    canvas = FigureCanvas(fig)
    canvas.draw()
    im = QImage(canvas.buffer_rgba(), IMAGE_WIDTH, IMAGE_HEIGHT, QImage.Format_ARGB32)
    return QPixmap(im)