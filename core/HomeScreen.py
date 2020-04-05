from easygui import msgbox
from matplotlib.figure import Figure
from utils.PlotClass import PlotRunnable
from core.QtWaitingSpinner import QtWaitingSpinner
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from controllers.CaricoManager import *
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QDateEdit, QSizePolicy,
                             QSpacerItem, QFrame, QMenuBar, QGridLayout, QListWidget, QStackedLayout, QCheckBox)
from utils.UtilsFunction import FigureToQPixmap,createLabel
from utils.MyLogger import writeLog

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        #Inizializzazione delle variabili che servono a creare il grafico
        data_corrente = QDate.currentDate()
        self.data = {
            "booking_ticket_departure_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "booking_ticket_arrival_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": "",
            "year_graphics": True #Checkbox anno
        }


    def go_to_home(self):
        idx = self.stack.currentIndex()
        print(idx)
        if idx == 1:
            self.stack.setCurrentIndex(0)

    def go_to_analytics(self):
        idx = self.stack.currentIndex()
        print(idx)
        if idx == 0:
            self.stack.setCurrentIndex(1)

    def searchLabel(self):
        horizontal_label = QHBoxLayout()
        horizontal_label.setContentsMargins(-1, 1, -1, -1)
        horizontal_label.setSpacing(15)
        horizontal_label.setObjectName("horizontal_label")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        horizontal_label.addItem(spacerItem)
        horizontal_label.addWidget(createLabel(self.verticalLayoutWidget, "label_tratta", "Tratta"))
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
        self.tratta_combobox = self.tratta_filter_selectbox()
        self.horizontal_filter.addWidget(self.tratta_combobox)
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

    def menu_button(self):
        self.layout_button_menu = QVBoxLayout()
        self.layout_button_menu.setSpacing(15)
        self.layout_button_menu.setObjectName("layout_button_menu")
        spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout_button_menu.addItem(spacerItem8)
        self.home_button = QPushButton(self.centralwidget)
        self.home_button.setObjectName("pushButton_2")
        self.home_button.clicked.connect(self.go_to_home)
        self.home_button.setText("HOME")
        self.layout_button_menu.addWidget(self.home_button)
        self.analytics_button = QPushButton(self.centralwidget)
        self.analytics_button.clicked.connect(self.go_to_analytics)
        self.analytics_button.setObjectName("pushButton")
        self.analytics_button.setText("ANALYTICS")
        self.layout_button_menu.addWidget(self.analytics_button)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout_button_menu.addItem(spacerItem9)
        self.body_layout.addLayout(self.layout_button_menu)

    def body(self):
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(-1, -1, -1, 0)
        self.body_layout.setSpacing(21)
        self.body_layout.setObjectName("body_layout")
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.body_layout.addItem(spacerItem8)
        self.menu_button()
        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.body_layout.addWidget(self.line)
        self.placeholder_image = QPixmap(PLACEHOLDER_PATH)
        self.placeholder_image = self.placeholder_image.scaledToWidth(IMAGE_WIDTH)
        self.statistics_image = QLabel(self.verticalLayoutWidget)
        self.statistics_image.setPixmap(self.placeholder_image)
        self.statistics_image.setAlignment(Qt.AlignCenter)
        self.statistics_image.setObjectName("statistics_image")
        self.spinner = QtWaitingSpinner(self)
        self.stack = QStackedLayout()
        self.stack.addWidget(self.statistics_image)
        self.stack.addWidget(createLabel(self.verticalLayoutWidget, "label_tratta", "Tratta"))
        self.stack.addWidget(self.spinner)
        self.body_layout.addLayout(self.stack)
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
        self.label_version = QLabel(self.verticalLayoutWidget)
        self.label_version.setObjectName("label_version")
        footer_layout.addWidget(self.label_version)
        self.verticalLayout.addLayout(footer_layout)

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
        self.searchArea()
        self.body()
        self.footer()
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
        self.create_graphics.setText(_translate("MainWindow", "Genera grafico"))
        self.clear_filter.setText(_translate("MainWindow", "Azzera filtri"))

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
            self.spinner.start()
            self.stack.setCurrentIndex(2)
            runnable = PlotRunnable(self)
            QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(Figure)
    def set_image_carico(self, figure):
        self.spinner.stop()
        self.stack.setCurrentIndex(0)
        self.show_image(figure)

    @pyqtSlot(str)
    def error_cargo_not_found(self,text):
        self.spinner.stop()
        msgbox(text)


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
            "booking_ticket_departure_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "booking_ticket_arrival_timestamp": data_corrente.toString("yyyy-MM-dd"),
            "ship": [],
            "departure_port_code": "",
            "arrival_port_code": ""
        }
        self.nave_combobox.clearSelection()
        self.tratta_combobox.setCurrentIndex(0)
        self.statistics_image.setPixmap(self.placeholder_image)
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

    def set_tratta(self, text):
        writeLog(levelLog.INFO, "App", "Tratta selezionata: {}".format(text))
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
        writeLog(levelLog.INFO, "App", "Data inizio selezionata: {}".format(data.toString("yyyy-MM-dd")))
        self.data["booking_ticket_departure_timestamp"] = data.toString("yyyy-MM-dd")

    def set_end_data(self, data):
        writeLog(levelLog.INFO, "App", "Data fine selezionata: {}".format(data.toString("yyyy-MM-dd")))
        self.data["booking_ticket_arrival_timestamp"] = data.toString("yyyy-MM-dd")
