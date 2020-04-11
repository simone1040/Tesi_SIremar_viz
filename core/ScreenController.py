from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton

from core.HomeScreen import HomeScreen
from core.AnalyticsScreen import AnalyticsScreen
from core.OptimizationScreen import OptimizationScreen
from utils.Costants import HOME_SCREEN, ANALYTICS_SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT,OPTIMIZATION_SCREEN


class ScreenController:
    __instance = None

    @staticmethod
    def getInstance(mainWindow = None):
        """ Static access method. """
        if ScreenController.__instance == None:
            ScreenController(mainWindow)
        return ScreenController.__instance

    def __init__(self, main_window):
        super().__init__()
        if ScreenController.__instance != None:
            raise Exception("Singleton")
        self.mainWindow = main_window
        self.mainWindow.setWindowTitle("Siremar Analitycs")
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = {
            HOME_SCREEN: HomeScreen(self),
            ANALYTICS_SCREEN: AnalyticsScreen(self),
            OPTIMIZATION_SCREEN: OptimizationScreen(self)
        }
        self.stack_widget = QStackedWidget(self.mainWindow)
        self.__initUserInterfaceScreen()
        self.__defineStackWidget()
        self.mainWindow.setCentralWidget(self.stack_widget)
        QMetaObject.connectSlotsByName(self.mainWindow)
        self.actual_screen = -1
        self.__change_screen(HOME_SCREEN)
        ScreenController.__instance = self

    def __initUserInterfaceScreen(self):
        self.screen[HOME_SCREEN].init_UI(self.mainWindow)
        self.screen[OPTIMIZATION_SCREEN].init_UI(self.mainWindow)
        self.screen[ANALYTICS_SCREEN].init_UI(self.mainWindow)

    def __defineStackWidget(self):
        self.stack_widget.addWidget(self.screen[HOME_SCREEN].centralwidget)
        self.stack_widget.addWidget(self.screen[OPTIMIZATION_SCREEN].centralwidget)
        self.stack_widget.addWidget(self.screen[ANALYTICS_SCREEN].centralwidget)

    def __change_screen(self, screen_to_show):
        if self.actual_screen == -1:
            self.stack_widget.setCurrentIndex(HOME_SCREEN)
            self.mainWindow.show()
        elif screen_to_show != self.actual_screen:
            self.stack_widget.setCurrentIndex(screen_to_show)
        self.actual_screen = screen_to_show

    def left_menu_button(self):
        layout_button_menu = QVBoxLayout()
        layout_button_menu.setSpacing(15)
        layout_button_menu.setObjectName("layout_button_menu")
        spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout_button_menu.addItem(spacerItem8)
        home_button = QPushButton()
        home_button.setObjectName("pushButton_2")
        home_button.clicked.connect(lambda: self.__change_screen(HOME_SCREEN))
        home_button.setText("HOME")
        layout_button_menu.addWidget(home_button)
        optimization_button = QPushButton()
        optimization_button.clicked.connect(lambda: self.__change_screen(OPTIMIZATION_SCREEN))
        optimization_button.setObjectName("pushButton")
        optimization_button.setText("OTTIMIZZAZIONE CARICO")
        layout_button_menu.addWidget(optimization_button)
        analytics_button = QPushButton()
        analytics_button.clicked.connect(lambda: self.__change_screen(ANALYTICS_SCREEN))
        analytics_button.setObjectName("pushButton")
        analytics_button.setText("ANALYTICS")
        layout_button_menu.addWidget(analytics_button)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_button_menu.addItem(spacerItem9)
        return layout_button_menu







