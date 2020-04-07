from easygui import msgbox
from utils.PlotClass import PlotRunnable
from PyQt5.QtCore import *
from controllers.CaricoManager import *
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QDateEdit, QSizePolicy,
                             QSpacerItem, QFrame, QGridLayout, QListWidget,QCheckBox, QPlainTextEdit)
from utils.UtilsFunction import createLabel
from utils.MyLogger import writeLog

class OptimizationScreen(QWidget):
    def __init__(self, screenController):
        super().__init__()
        #Inizializzazione delle variabili che servono a creare il grafico
        self.screenController = screenController
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "booking_ticket_arrival_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": "",
            "year_graphics": True #Checkbox anno
        }

    def searchLabel(self):
        horizontal_label = QHBoxLayout()
        horizontal_label.setContentsMargins(-1, 1, -1, -1)
        horizontal_label.setSpacing(15)
        horizontal_label.setObjectName("horizontal_label")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        horizontal_label.addItem(spacerItem)
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_nave", "Nave"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_data_partenza", "Data partenza"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_data_arrivo", "Data arrivo"))
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_anno", "Anno"))
        horizontal_label.addItem(spacerItem)
        self.verticalLayout.addLayout(horizontal_label)

    def checkbox_anno(self):
        checkBox = QCheckBox(self.centralwidget)
        checkBox.setText("")
        checkBox.setChecked(True)
        checkBox.setStyleSheet("QCheckBox::indicator {\n"
                                    "     width: 20px;\n"
                                    "     height: 20px;\n"
                                    "}")
        checkBox.setObjectName("checkBox")
        checkBox.stateChanged.connect(self.set_checkbox_year_status)
        return checkBox

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

    def searchArea(self):
        self.searchLabel()
        self.horizontal_filter = QHBoxLayout()
        self.horizontal_filter.setContentsMargins(-1, -1, -1, 10)
        self.horizontal_filter.setSpacing(15)
        self.horizontal_filter.setObjectName("horizontal_filter")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem2)
        self.nave_combobox = self.ship_filter_selectbox()
        self.horizontal_filter.addWidget(self.nave_combobox)
        self.data_partenza_selector = self.init_data_selectbox()
        self.horizontal_filter.addWidget(self.data_partenza_selector)
        self.data_arrivo_selector = self.end_data_selectbox()
        self.horizontal_filter.addWidget(self.data_arrivo_selector)
        self.checkBox = self.checkbox_anno()
        self.horizontal_filter.addWidget(self.checkBox)
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
        self.text_area_optimization = QPlainTextEdit(self.centralwidget)
        self.text_area_optimization.setMinimumSize(QSize(1000, 770))
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

    def footer(self):
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(-1, -1, -1, 5)
        footer_layout.setSpacing(6)
        footer_layout.setObjectName("footer_layout")
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        footer_layout.addItem(spacerItem10)
        label_product_by = QLabel(self.verticalLayoutWidget)
        label_product_by.setObjectName("label_product_by")
        label_product_by.setText("Copyright Simone Condorelli")
        footer_layout.addWidget(label_product_by)
        spacerItem11 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        footer_layout.addItem(spacerItem11)
        label_5 = QLabel(self.verticalLayoutWidget)
        label_5.setObjectName("label_5")
        label_5.setText("Version :")
        footer_layout.addWidget(label_5)
        spacerItem12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        footer_layout.addItem(spacerItem12)
        label_version = QLabel(self.verticalLayoutWidget)
        label_version.setObjectName("label_version")
        label_version.setText(VERSION)
        footer_layout.addWidget(label_version)
        self.verticalLayout.addLayout(footer_layout)

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
        self.footer()
        self.verticalLayout.addStretch()
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

    def function_create_statistics(self):
        if self.data["booking_ticket_departure_timestamp"] > self.data["booking_ticket_arrival_timestamp"]:
            msgbox("La data di partenza non può essere più piccola della data di arrivo")
        else:
            #TODO FUNZIONE CHE SCRIVERÀ SU TEXT-AREA
            runnable = PlotRunnable(self)


    def ship_filter_selectbox(self):
        cb = QListWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cb.sizePolicy().hasHeightForWidth())
        cb.setSizePolicy(sizePolicy)
        cb.setMaximumSize(QSize(16777215, 60))
        cb.setObjectName("nave_combobox")
        cb.setToolTip("Selezionare una o più navi per effettuare l'ottimizzazione del carico.")
        cb.setSelectionMode(QListWidget.MultiSelection)
        cb.itemClicked.connect(self.set_ship)
        dataframe = get_distinct_ship()
        for index, row in dataframe.iterrows():
            cb.addItem(row["ship_code"]+"-"+row["ship_name"])
        return cb

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
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }
        self.nave_combobox.clearSelection()
        self.data_partenza_selector.setDate(data_corrente)
        self.data_arrivo_selector.setDate(data_corrente)

    def set_checkbox_year_status(self):
        if self.checkBox.isChecked():
            self.data["year_graphics"] = True
            writeLog(levelLog.INFO, "App", "Filtro checked")
        else:
            self.data["year_graphics"] = False
            writeLog(levelLog.INFO, "App", "Filtro unchecked")

    def set_ship(self, ship):
        ship = ship.text()
        ship_code, ship_name = ship.split("-")
        writeLog(levelLog.INFO, "App", "Nave selezionata: {}".format(ship))
        if ship_code in self.data["ship"]:
            self.data["ship"].remove(ship_code)
        else:
            self.data["ship"].append(ship_code)
        writeLog(levelLog.INFO,"App","Navi rimanenti: {}".format(self.data["ship"]))

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
        writeLog(levelLog.INFO, "App", "Data inizio selezionata: {}".format(data.toString("yyyy-MM-dd")))
        self.data["booking_ticket_departure_timestamp"] = data.toString("yyyy-MM-dd")

    def set_end_data(self, data):
        writeLog(levelLog.INFO, "App", "Data fine selezionata: {}".format(data.toString("yyyy-MM-dd")))
        self.data["booking_ticket_arrival_timestamp"] = data.toString("yyyy-MM-dd")