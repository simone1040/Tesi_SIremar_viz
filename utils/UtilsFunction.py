from PyQt5.QtWidgets import QLabel
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from utils.Costants import IMAGE_HEIGHT,IMAGE_WIDTH
from PyQt5.QtGui import QImage, QPixmap
import pandas as pd

def FigureToQPixmap(fig):
    canvas = FigureCanvas(fig)
    canvas.draw()
    im = QImage(canvas.buffer_rgba(), IMAGE_WIDTH, IMAGE_HEIGHT, QImage.Format_ARGB32)
    return QPixmap(im)

def createLabel(parent,object_name,text):
        label = QLabel(parent)
        label.setObjectName(object_name)
        label.setText(text)
        return label

#Restituisce il dataframe che utilizziamo per stampare le informazioni
def get_dataframe_data_to_show():
    return pd.DataFrame(columns=["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
                 "metri_garage_navi_spazio_totale","tot_mq_occupati"])

