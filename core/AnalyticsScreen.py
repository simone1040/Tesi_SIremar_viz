from easygui import msgbox
from PyQt5.QtCore import *

from controllers.AnalyticsController import AnalyticsController
from controllers.CaricoManager import *
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QDateEdit, QSizePolicy,
                             QSpacerItem, QFrame, QGridLayout, QListWidget,QPlainTextEdit, QTableWidget,
                             QHeaderView, QTableWidgetItem, QComboBox)
from utils.UtilsFunction import createLabel
from utils.MyLogger import writeLog
from core.CommonWidget import footer

class AnalyticsScreen(QWidget):
    __distinct_ship = None

    def __init__(self, screenController):
        super().__init__()
        #Inizializzazione delle variabili che servono a creare il grafico
        self.screenController = screenController
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "booking_ticket_arrival_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "ship_code_selected": [],
            "ship_name_selected": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }

    def searchLabel(self):
        horizontal_label = QHBoxLayout()
        horizontal_label.setContentsMargins(-1, 1, -1, -1)
        horizontal_label.setSpacing(15)
        horizontal_label.setObjectName("horizontal_label")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        horizontal_label.addItem(spacerItem)
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_tratta", "Tratta"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_data_partenza", "Data partenza"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_data_arrivo", "Data arrivo"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_nave", "Nave/i"))
        horizontal_label.addItem(spacerItem)
        self.verticalLayout.addLayout(horizontal_label)

    def button_action(self):
        self.horizontalButton = QHBoxLayout()
        self.horizontalButton.setObjectName("horizontalButton")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem4)
        self.create_graphics = self.create_statistics_push_button()
        self.horizontalButton.addWidget(self.create_graphics)
        self.clear_filter = self.clear_filter_search_data()
        self.horizontalButton.addWidget(self.clear_filter)
        self.clear_text_area = self.button_clear_text_area()
        self.horizontalButton.addWidget(self.clear_text_area)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalButton)

    def set_tratta(self, text):
        writeLog(levelLog.INFO, "App", "Tratta selezionata: {}".format(text))
        port = text.split("-")
        if(len(port) == 2):
            if self.data["departure_port_code"] != port[0] or self.data["arrival_port_code"] != port[1]:
                self.data["departure_port_code"], self.data["arrival_port_code"] = port
                self.popolateComboBoxShip()
        else:
            self.data["departure_port_code"] = self.data["arrival_port_code"] = ""
            try:
                self.popolateComboBoxShip()
            except:
                self.nave_combobox = None

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

    def searchArea(self):
        self.searchLabel()
        self.horizontal_filter = QHBoxLayout()
        self.horizontal_filter.setContentsMargins(-1, -1, -1, 10)
        self.horizontal_filter.setSpacing(15)
        self.horizontal_filter.setObjectName("horizontal_filter")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem2)
        self.tratta_combobox = self.tratta_filter_selectbox()
        self.horizontal_filter.addWidget(self.tratta_combobox)
        self.data_partenza_selector = self.init_data_selectbox()
        self.horizontal_filter.addWidget(self.data_partenza_selector)
        self.data_arrivo_selector = self.end_data_selectbox()
        self.horizontal_filter.addWidget(self.data_arrivo_selector)
        self.nave_combobox = self.ship_filter_selectbox_to_optimize()
        self.horizontal_filter.addWidget(self.nave_combobox)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontal_filter)
        self.button_action()
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

    def table_widget(self):
        tableWidget = QTableWidget(self.centralwidget)
        tableWidget.setColumnCount(2)
        tableWidget.setRowCount(0)
        tableWidget.setHorizontalHeaderLabels(["Nave", "Capienza Massima"])
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.setObjectName("tableWidget")
        return tableWidget

    def body(self):
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(-1, -1, -1, 0)
        self.body_layout.setSpacing(21)
        self.body_layout.setObjectName("body_layout")
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.body_layout.addItem(spacerItem8)
        self.body_layout.addLayout(self.screenController.left_menu_button())
        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.body_layout.addWidget(self.line)
        self.tableWidget = self.table_widget()
        self.body_layout.addWidget(self.tableWidget)
        self.text_area_optimization = QPlainTextEdit(self.centralwidget)
        self.text_area_optimization.setMinimumSize(QSize(250, 763))
        self.text_area_optimization.setReadOnly(True)
        self.text_area_optimization.setObjectName("text_area_optimization")
        self.body_layout.addWidget(self.text_area_optimization)
        self.verticalLayout.addLayout(self.body_layout)
        spacerItem8 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
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

    def init_UI(self, MainWindow):
        #Inizializzazione dell'interfaccia grafica
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
        self.searchArea()
        self.body()
        footer_layout = footer(self.verticalLayoutWidget)
        self.verticalLayout.addLayout(footer_layout)
        self.verticalLayout.addStretch()
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

    def function_create_statistics(self):
        print(self.data["ship_code_selected"])
        print(len(self.data["ship_code_selected"]))
        if self.data["booking_ticket_departure_timestamp"] > self.data["booking_ticket_arrival_timestamp"]:
            msgbox("La data di partenza non può essere più piccola della data di arrivo")
        elif self.data["departure_port_code"] == "" or self.data["arrival_port_code"] == "":
            msgbox("Nessuna tratta scelta.")
        elif len(self.data["ship_code_selected"]) < 2:
            msgbox("Scegliere almeno due navi per poter effettuare l'ottimizzazione.")
        else:
            self.writeToTextArea("Tratta selezionata --> {}-{}".format(self.data["departure_port_code"], self.data["arrival_port_code"]))
            res = AnalyticsController(self).getStatistics()

    def clearTable(self):
        self.tableWidget.setRowCount(0)

    def setElementInTable(self, array_of_ship):
        row_count = len(array_of_ship)
        self.tableWidget.setRowCount(row_count)
        for index, nave in zip(range(0, row_count), array_of_ship):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(nave.getNaveName()))) #Nome nave
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(nave.getCapienzaMassima()) + " mq")) #Mq nave

    def popolateComboBoxShip(self):
        ship_code, ship_name = AnalyticsController(self).getNaviWithSameTripAndHour(self.data["departure_port_code"],
                                                          self.data["arrival_port_code"],
                                                          self.data["booking_ticket_departure_timestamp"],
                                                          self.data["booking_ticket_arrival_timestamp"])
        if len(ship_code) == 0:
            self.nave_combobox.clear()
            self.nave_combobox.setEnabled(False)
        else:
            for nave_code, nave_name in zip(ship_code, ship_name):
                self.nave_combobox.addItem(nave_code+"-"+nave_name)
                self.nave_combobox.setEnabled(True)

    def writeToTextArea(self, text):
        self.text_area_optimization.appendPlainText(text)

    # SelectBox per la singola nave da ottimizzare
    def ship_filter_selectbox_to_optimize(self):
        cb = QListWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cb.sizePolicy().hasHeightForWidth())
        cb.setSizePolicy(sizePolicy)
        cb.setMaximumSize(QSize(16777215, 60))
        cb.setEnabled(False)
        cb.itemClicked.connect(self.set_ship)
        cb.setSelectionMode(QListWidget.MultiSelection)
        cb.setObjectName("nave_combobox")
        cb.setToolTip("Selezionare una nave per effettuare l'ottimizzazione del carico.")
        return cb

    def set_ship(self, ship):
        ship = ship.text()
        ship_code, ship_name = ship.split("-")
        if ship_code in self.data["ship_code_selected"]:
            self.data["ship_code_selected"].remove(ship_code)
            self.data["ship_name_selected"].remove(ship_name)
        else:
            self.data["ship_code_selected"].append(ship_code)
            self.data["ship_name_selected"].append(ship_name)

    def clear_filter_search_data(self):
        cf = QPushButton(self.verticalLayoutWidget)
        cf.setObjectName("clear_filter")
        cf.setText("Azzera filtri")
        cf.clicked.connect(self.function_clear_filter)
        return cf

    def create_statistics_push_button(self):
        pb = QPushButton(self.verticalLayoutWidget)
        pb.setLayoutDirection(Qt.LeftToRight)
        pb.setText("Calcola Ottimizzazione")
        pb.setToolTip("Procedura che cerca di individuare una nave che ottimizza il carico della nave selezionata.")
        pb.clicked.connect(self.function_create_statistics)
        pb.setObjectName("create_graphics")
        return pb

    def clear_text_area(self):
        self.text_area_optimization.clear()

    def button_clear_text_area(self):
        pb = QPushButton(self.verticalLayoutWidget)
        pb.setLayoutDirection(Qt.LeftToRight)
        pb.setText("Azzera Area Testuale")
        pb.clicked.connect(self.clear_text_area)
        pb.setObjectName("clear_text_area")
        return pb

    def function_clear_filter(self):
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "booking_ticket_arrival_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "ship_code_selected": [],
            "ship_name_selected": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }
        self.clearTable()
        self.nave_combobox.clearSelection()
        self.tratta_combobox.setCurrentIndex(0)
        self.data_partenza_selector.setDate(data_corrente)
        self.data_arrivo_selector.setDate(data_corrente)

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
        if data.toString("yyyy-MM-dd") != self.data["booking_ticket_departure_timestamp"]:
            writeLog(levelLog.INFO, "App", "Data inizio selezionata: {}".format(data.toString("yyyy-MM-dd")))
            self.data["booking_ticket_departure_timestamp"] = data.toString("yyyy-MM-dd")
            self.popolateComboBoxShip()

    def set_end_data(self, data):
        if data.toString("yyyy-MM-dd") != self.data["booking_ticket_arrival_timestamp"]:
            writeLog(levelLog.INFO, "App", "Data fine selezionata: {}".format(data.toString("yyyy-MM-dd")))
            self.data["booking_ticket_arrival_timestamp"] = data.toString("yyyy-MM-dd")
            self.popolateComboBoxShip()
