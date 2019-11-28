from utils.Costants import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QImage, QPixmap
from utils.CaricoManager import *
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QRadioButton, QVBoxLayout, QWidget, QComboBox, QCalendarWidget, QDateEdit, QSizePolicy, QSpacerItem,
    QFrame, QStatusBar, QMenuBar, QMainWindow)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

    def init_UI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1281, 751))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_label = QHBoxLayout()
        self.horizontal_label.setContentsMargins(-1, 10, -1, -1)
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
        self.tratta_combobox = self.port_code_selectbox()
        self.horizontal_filter.addWidget(self.tratta_combobox)
        self.nave_combobox = QComboBox(self.verticalLayoutWidget)
        self.nave_combobox.setObjectName("nave_combobox")
        self.horizontal_filter.addWidget(self.nave_combobox)
        self.data_partenza_selector = QDateEdit(self.verticalLayoutWidget)
        self.data_partenza_selector.setObjectName("data_partenza_selector")
        self.horizontal_filter.addWidget(self.data_partenza_selector)
        self.data_arrivo_selector = QDateEdit(self.verticalLayoutWidget)
        self.data_arrivo_selector.setObjectName("data_arrivo_selector")
        self.horizontal_filter.addWidget(self.data_arrivo_selector)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontal_filter.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontal_filter)
        self.horizontalButton = QHBoxLayout()
        self.horizontalButton.setObjectName("horizontalButton")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem4)
        self.create_graphics = QPushButton(self.verticalLayoutWidget)
        self.create_graphics.setLayoutDirection(Qt.LeftToRight)
        self.create_graphics.setObjectName("create_graphics")
        self.horizontalButton.addWidget(self.create_graphics)
        self.clear_filter = QPushButton(self.verticalLayoutWidget)
        self.clear_filter.setObjectName("clear_filter")
        self.horizontalButton.addWidget(self.clear_filter)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalButton.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalButton)
        self.horizontalSpacer_2 = QHBoxLayout()
        self.horizontalSpacer_2.setContentsMargins(-1, -1, -1, 5)
        self.horizontalSpacer_2.setObjectName("horizontalSpacer_2")
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalSpacer_2.addItem(spacerItem6)
        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalSpacer_2.addWidget(self.line)
        spacerItem7 = QSpacerItem(40, 18, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalSpacer_2.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalSpacer_2)
        self.statistics_image = QLabel(self.verticalLayoutWidget)
        self.statistics_image.setText("")
        self.statistics_image.setPixmap(QPixmap(PLACEHOLDER_PATH))
        self.statistics_image.setAlignment(Qt.AlignCenter)
        self.statistics_image.setObjectName("statistics_image")
        self.verticalLayout.addWidget(self.statistics_image)
        spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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


    def init_UI_OLD(self):
        # Impostazione finestra a dimensioni fisse
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Icona e titolo della finestra dell'applicazione
        self.setWindowTitle(APP_TITLE)

        # Creazione dell'immagine principale
        self.qlabel = QLabel(self)
        self.pixmap = QPixmap(PLACEHOLDER_PATH)
        self.pixmap = self.pixmap.scaledToHeight(IMAGE_HEIGHT)
        self.qlabel.setPixmap(self.pixmap)
        #Creazione del selectbox per la tratta
        self.departure_port_code = None
        self.arrival_port_code = None
        self.cb = self.port_code_selectbox()

        #aggiunta del selezionatore di data
        self.init_data_range = self.init_data_selectbox()
        self.end_data_range = self.end_data_selectbox()

        #aggiunta delle label dei filtri di ricerca
        labelSelectTratta = QLabel(self)
        labelSelectTratta.setText("Tratta")

        # Allineamento al centro del frame
        self.qlabel.setAlignment(Qt.AlignCenter)
        # Viene impiegato un layout di tipo Box, con un box verticale contentente
        #HBOX0 PER LE LABEL

        self.hbox0 = QHBoxLayout()
        self.hbox0.addWidget(labelSelectTratta, alignment=Qt.AlignLeft)
        
        # HBOX1 serve per i parametri di ricerca
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.cb, alignment=Qt.AlignLeft)
        self.hbox1.addWidget(self.init_data_range, alignment=Qt.AlignLeft)
        self.hbox1.addWidget(self.end_data_range, alignment=Qt.AlignLeft)
        self.vbox = QVBoxLayout()

        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addWidget(self.qlabel)

        # Impostazione del layout, appena creato, nell'applicazione
        self.setLayout(self.vbox)

        self.show()

    def port_code_selectbox(self):
        cb = QComboBox(self.verticalLayoutWidget)
        cb.setObjectName("tratta_combobox")
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


    def init_data_selectbox(self):
        date_edit = QDateEdit(self.verticalLayoutWidget)
        date_edit.setCalendarPopup(True)
        return date_edit

    def end_data_selectbox(self):
        date_edit = QDateEdit(self.verticalLayoutWidget)
        date_edit.setCalendarPopup(True)
        return date_edit