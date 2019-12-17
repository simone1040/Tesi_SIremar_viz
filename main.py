from pyspark.shell import spark
from pyspark.sql import SQLContext
import sys
from utils.Costants import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from core.App import MyApp
from utils.CaricoManager import compute_dataframe_tot_mq_occupati
from utils.CaricoManager import getMaxCaricoNave

if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    IMAGE_INFO["dpi_monitor"] = screen.physicalDotsPerInch()
    database_max_mq = getMaxCaricoNave()

    if(not database_max_mq.empty):
        DATAFRAME_APPLICATION["dataframe_max_mq_occupati"] = database_max_mq
    else:
        sys.exit(1)
    dataframe_prenotazioni = sqlContext.read.parquet(PARQUET_FILE_PRENOTATION).toPandas()
    if(not dataframe_prenotazioni.empty):
        DATAFRAME_APPLICATION["dataframe_prenotazioni"] = dataframe_prenotazioni
    else:
        sys.exit(1)

    DATAFRAME_APPLICATION["dataframe_tot_mq_occupati"] = compute_dataframe_tot_mq_occupati()
    my_app = MyApp()
    MainWindow = QMainWindow()
    my_app.init_UI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




