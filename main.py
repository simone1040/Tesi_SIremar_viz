from pyspark.shell import spark
from pyspark.sql import SQLContext
import sys
from utils.MyLogger import writeLog
from utils.Costants import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from core.ScreenController import ScreenController
from controllers.CaricoManager import getMaxCaricoNave

if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    IMAGE_INFO["dpi_monitor"] = screen.physicalDotsPerInch()
    database_max_mq = getMaxCaricoNave()
    if not database_max_mq.empty:
        DATAFRAME_APPLICATION["dataframe_max_mq_occupati"] = database_max_mq
        writeLog(levelLog.INFO, "main", "dataframe max mq occupati caricato correttamente")
    else:
        writeLog(levelLog.ERROR, "main", "dataframe max mq occupati non trovato")
        sys.exit(1)

    dataframe_prenotazioni = sqlContext.read.parquet(PARQUET_FILE_PRENOTATION).toPandas()
    if not dataframe_prenotazioni.empty:
        DATAFRAME_APPLICATION["dataframe_prenotazioni"] = dataframe_prenotazioni
        writeLog(levelLog.INFO, "main", "dataframe prenotazioni caricato correttamente")
    else:
        writeLog(levelLog.ERROR, "main", "dataframe prenotazioni non trovato")
        sys.exit(1)

    MainWindow = QMainWindow()
    screen_Controller = ScreenController.getInstance(mainWindow=MainWindow)
    sys.exit(app.exec_())



