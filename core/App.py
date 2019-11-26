from utils.Costants import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QImage, QPixmap
from utils.CaricoManager import *
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QRadioButton, QVBoxLayout, QWidget, QComboBox, QCalendarWidget)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()


    def init_UI(self):
        # Impostazione finestra a dimensioni fisse
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Icona e titolo della finestra dell'applicazione
        self.setWindowTitle(APP_TITLE)

        # Creazione dell'immagine principale
        self.qlabel = QLabel(self)
        self.pixmap = QPixmap(PLACEHOLDER_PATH)
        self.pixmap = self.pixmap.scaledToHeight(IMAGE_HEIGHT)
        self.departure_port_code = None
        self.arrival_port_code = None
        self.cb = self.port_code_selectbox()
        self.qlabel.setPixmap(self.pixmap)
        # Allineamento al centro del frame
        self.qlabel.setAlignment(Qt.AlignCenter)
        # Viene impiegato un layout di tipo Box, con un box verticale contentente
        # l'immagine principale e i tre box orizzontali (uno per textbox e pulsanti, uno per i radio buttons
        # per la selezione della rete neurale da utilizzare e uno per i messaggi in-app)
        self.hbox1 = QHBoxLayout()
        self.hbox1.setContentsMargins(0,20,0,0)
        self.hbox1.addWidget(self.cb, alignment=Qt.AlignLeft)
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addWidget(self.qlabel)

        # Impostazione del layout, appena creato, nell'applicazione
        self.setLayout(self.vbox)

        self.show()

    def port_code_selectbox(self):
        cb = QComboBox()
        cb.setFixedSize(400, 25)
        cb.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        cb.setMaxVisibleItems(10)
        cb.setStyleSheet("QComboBox { combobox-popup: 0; }")
        #Funzione che deve essere effettuata quando cambia elemento nella lista
        cb.currentTextChanged.connect(self.update_port)
        dataframe = get_distinct_tratte()
        for index, row in dataframe.iterrows():
            if(row["booking_ticket_departure_port_code"] != "" and row["booking_ticket_arrival_port_code"] != ""):
                cb.addItem(row["booking_ticket_departure_port_code"]+"-"+row["booking_ticket_arrival_port_code"])
        return cb

    def update_port(self, text):
        port = text.split("-")
        if(len(port) == 2):
            self.departure_port_code = port[0]
            self.arrival_port_code = port[1]

