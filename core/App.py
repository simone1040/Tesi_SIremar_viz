from easygui import msgbox

from utils import CaricoManager
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from utils.CaricoManager import *
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QDateEdit, QSizePolicy,
                             QSpacerItem, QFrame, QMenuBar, QGridLayout, QListWidget)
from utils.UtilsFunction import FigureToQPixmap


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        #Inizializzazione delle variabili che servono a creare il grafico
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente,
            "booking_ticket_arrival_timestamp": data_corrente,
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }

    def init_UI(self, MainWindow):
        #Inizializzazione dell'interfaccia grafica
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_label = QHBoxLayout()
        self.horizontal_label.setContentsMargins(-1, 1, -1, -1)
        self.horizontal_label.setSpacing(15)
        self.horizontal_label.setObjectName("horizontal_label")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_label.addItem(spacerItem)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontal_label.addWidget(self.label_2)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontal_label.addWidget(self.label_3)
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontal_label.addWidget(self.label_4)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontal_label.addWidget(self.label)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_label.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontal_label)
        self.horizontal_filter = QHBoxLayout()
        self.horizontal_filter.setContentsMargins(-1, -1, -1, 10)
        self.horizontal_filter.setSpacing(15)
        self.horizontal_filter.setObjectName("horizontal_filter")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem2)
        self.tratta_combobox = self.tratta_filter_selectbox()
        self.horizontal_filter.addWidget(self.tratta_combobox)
        self.nave_combobox = self.ship_filter_selectbox()
        self.horizontal_filter.addWidget(self.nave_combobox)
        self.data_partenza_selector = self.init_data_selectbox()
        self.horizontal_filter.addWidget(self.data_partenza_selector)
        self.data_arrivo_selector = self.end_data_selectbox()
        self.horizontal_filter.addWidget(self.data_arrivo_selector)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontal_filter)
        self.horizontalButton = QHBoxLayout()
        self.horizontalButton.setObjectName("horizontalButton")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem4)
        self.create_graphics = self.create_statistics_push_button()
        self.horizontalButton.addWidget(self.create_graphics)
        self.clear_filter = self.clear_filter_search_data()
        self.horizontalButton.addWidget(self.clear_filter)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalButton)
        self.top_separator_layout = QHBoxLayout()
        self.top_separator_layout.setContentsMargins(-1, -1, -1, 5)
        self.top_separator_layout.setObjectName("top_separator_layout")
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.top_separator_layout.addItem(spacerItem6)
        self.top_separator_line = QFrame(self.verticalLayoutWidget)
        self.top_separator_line.setFrameShape(QFrame.HLine)
        self.top_separator_line.setFrameShadow(QFrame.Sunken)
        self.top_separator_line.setObjectName("top_separator_line")
        self.top_separator_layout.addWidget(self.top_separator_line)
        spacerItem7 = QSpacerItem(40, 18, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.top_separator_layout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.top_separator_layout)
        self.placeholder_image = QPixmap(PLACEHOLDER_PATH)
        self.placeholder_image = self.placeholder_image.scaledToWidth(IMAGE_WIDTH)
        self.statistics_image = QLabel(self.verticalLayoutWidget)
        self.statistics_image.setPixmap(self.placeholder_image)
        self.statistics_image.setAlignment(Qt.AlignCenter)
        self.statistics_image.setObjectName("statistics_image")
        self.verticalLayout.addWidget(self.statistics_image)
        spacerItem8 = QSpacerItem(20,45, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem8)
        self.bottom_separator_layout = QHBoxLayout()
        self.bottom_separator_layout.setContentsMargins(-1, -1, -1, 5)
        self.bottom_separator_layout.setObjectName("top_separator_layout")
        spacerItem6 = QSpacerItem(40, 25, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.bottom_separator_layout.addItem(spacerItem6)
        self.bottom_separator_line = QFrame(self.verticalLayoutWidget)
        self.bottom_separator_line.setFrameShape(QFrame.HLine)
        self.bottom_separator_line.setFrameShadow(QFrame.Sunken)
        self.bottom_separator_line.setObjectName("top_separator_line")
        self.bottom_separator_layout.addWidget(self.bottom_separator_line)
        spacerItem7 = QSpacerItem(40, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.bottom_separator_layout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.bottom_separator_layout)
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(-1, -1, -1, 5)
        self.footer_layout.setSpacing(6)
        self.footer_layout.setObjectName("footer_layout")
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.footer_layout.addItem(spacerItem10)
        self.label_product_by = QLabel(self.verticalLayoutWidget)
        self.label_product_by.setObjectName("label_product_by")
        self.footer_layout.addWidget(self.label_product_by)
        spacerItem11 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.footer_layout.addItem(spacerItem11)
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.footer_layout.addWidget(self.label_5)
        spacerItem12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.footer_layout.addItem(spacerItem12)
        self.label_version = QLabel(self.verticalLayoutWidget)
        self.label_version.setObjectName("label_version")
        self.footer_layout.addWidget(self.label_version)
        self.verticalLayout.addLayout(self.footer_layout)
        self.verticalLayout.addStretch()
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1282, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Siremar Analitycs"))
        self.label_2.setText(_translate("MainWindow", "Tratta"))
        self.label_3.setText(_translate("MainWindow", "Nave"))
        self.label_4.setText(_translate("MainWindow", "Intervallo data partenza"))
        self.label.setText(_translate("MainWindow", "Intervallo data arrivo"))
        self.create_graphics.setText(_translate("MainWindow", "Genera grafico"))
        self.clear_filter.setText(_translate("MainWindow", "Azzera filtri"))
        self.label_product_by.setText(_translate("MainWindow", "Copyright Simone Condorelli"))
        self.label_5.setText(_translate("MainWindow", "Version :"))
        self.label_version.setText(_translate("MainWindow", VERSION))


    def tratta_filter_selectbox(self):
        cb = QComboBox(self.verticalLayoutWidget)
        cb.setObjectName("tratta_combobox")
        cb.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        cb.setMaxVisibleItems(10)
        cb.setStyleSheet("QComboBox { combobox-popup: 0; }")
        #Funzione che deve essere effettuata quando cambia elemento nella lista
        cb.currentTextChanged.connect(self.set_tratta)
        dataframe = get_distinct_tratte()
        #Primo elemento vuoto
        cb.addItem("Nessuna tratta selezionata")
        for index, row in dataframe.iterrows():
            if(row["booking_ticket_departure_port_code"] != "" and row["booking_ticket_arrival_port_code"] != ""):
                cb.addItem(row["booking_ticket_departure_port_code"]+"-"+row["booking_ticket_arrival_port_code"])
        return cb

    def function_create_statistics(self):
        if self.data["booking_ticket_departure_timestamp"] > self.data["booking_ticket_arrival_timestamp"]:
            msgbox("La data di partenza non può essere più piccola della data di arrivo")
        else:
            figure = CaricoManager.image_statistics_filtered(self.data)
            self.show_image(figure)

    def ship_filter_selectbox(self):
        cb = QListWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cb.sizePolicy().hasHeightForWidth())
        cb.setSizePolicy(sizePolicy)
        cb.setMaximumSize(QSize(16777215, 60))
        cb.setObjectName("nave_combobox")
        cb.setSelectionMode(QListWidget.MultiSelection)
        cb.itemClicked.connect(self.set_ship)
        dataframe = get_distinct_ship()
        for index, row in dataframe.iterrows():
            cb.addItem(row["ship_code"]+"-"+row["ship_name"])
        return cb

    def clear_filter_search_data(self):
        cf = QPushButton(self.verticalLayoutWidget)
        cf.setObjectName("clear_filter")
        cf.clicked.connect(self.function_clear_filter)
        return cf

    def create_statistics_push_button(self):
        pb = QPushButton(self.verticalLayoutWidget)
        pb.setLayoutDirection(Qt.LeftToRight)
        pb.clicked.connect(self.function_create_statistics)
        pb.setObjectName("create_graphics")
        return pb

    def function_clear_filter(self):
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente,
            "booking_ticket_arrival_timestamp": data_corrente,
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }
        self.nave_combobox.clearSelection()
        self.tratta_combobox.setCurrentIndex(0)
        self.statistics_image.setPixmap(self.placeholder_image)
        self.data_partenza_selector.setDate(data_corrente)
        self.data_arrivo_selector.setDate(data_corrente)

    def set_ship(self, ship):
        ship = ship.text()
        ship_code, ship_name = ship.split("-")
        if ship_code in self.data["ship"]:
            self.data["ship"].remove(ship_code)
        else:
            self.data["ship"].append(ship_code)

    def set_tratta(self, text):
        port = text.split("-")
        if(len(port) == 2):
            self.data["departure_port_code"], self.data["arrival_port_code"] = port
        else:
            self.data["departure_port_code"] = self.data["arrival_port_code"] = ""

    def show_image(self, figure):
        image = FigureToQPixmap(figure)
        image = image.scaledToWidth(IMAGE_WIDTH)
        self.statistics_image.setPixmap(image)

    def init_data_selectbox(self):
        date_edit = QDateEdit(self.verticalLayoutWidget)
        date_edit.dateChanged.connect(self.set_start_data)
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit

    def end_data_selectbox(self):
        date_edit = QDateEdit(self.verticalLayoutWidget)
        date_edit.dateChanged.connect(self.set_end_data)
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit

    def set_start_data(self, data):
        self.data["booking_ticket_departure_timestamp"] = data

    def set_end_data(self, data):
        self.data["booking_ticket_arrival_timestamp"] = data
