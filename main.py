from pyspark.shell import spark
from pyspark.sql import SQLContext
import sys
from utils.Costants import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from core.App import MyApp
from utils.CaricoManager import getMaxCaricoNave

if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    app = QApplication(sys.argv)
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

    my_app = MyApp()
    MainWindow = QMainWindow()
    my_app.init_UI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    """parser = argparse.ArgumentParser(description='Visualization of statistics')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-gmc', help="Plot dei carichi max della nave e salvataggio sulla cartella assets", action='store_true')
    g.add_argument('-cat', help="Stampa della categoria e dello spazio occupato per spazio inferiore e superiore a S18 per cargo", action='store_true')
    g.add_argument('-ctot', help="Stampa della categoria e dello spazio occupato totale per cargo", action='store_true')
    g.add_argument('-pre', help="Stampa della categoria e dello spazio occupato totale per prenotation", action='store_true')
    g.add_argument('-ptot', help="Stampa della categoria e dello spazio occupato totale per prenotation", action='store_true')
    args = parser.parse_args()

    if args.gmc:
        dataframe = getMaxCaricoNave()
        if not dataframe.empty:
            plotMaxCaricoNave(dataframe)

    if args.cat:
        print("CARICAMENTO DATAFRAME...\n")
        dataframe_max_mq = getMaxCaricoNave()
        dataframe = sqlContext.read.parquet(PARQUET_FILE_CARGO).toPandas()
        plotCaricoPerNave(dataframe, dataframe_max_mq)

    if args.ctot:
        print("CARICAMENTO DATAFRAME...\n")
        dataframe_max_mq = getMaxCaricoNave()
        dataframe = sqlContext.read.parquet(PARQUET_FILE_CARGO).toPandas()
        plotCaricoPerNaveTot(dataframe, dataframe_max_mq)

    if args.pre:
        print("CARICAMENTO DATAFRAME...\n")
        dataframe_max_mq = getMaxCaricoNave()
        dataframe = sqlContext.read.parquet(PARQUET_FILE_PRENOTATION).toPandas()
        plotCaricoPerNavePrenotazioni(dataframe, dataframe_max_mq)

    if args.ptot:
        print("CARICAMENTO DATAFRAME...\n")
        dataframe_max_mq = getMaxCaricoNave()
        dataframe = sqlContext.read.parquet(PARQUET_FILE_PRENOTATION).toPandas()
        plotCaricoPerNaveTotPrenotation(dataframe, dataframe_max_mq)"""




