from decimal import *

from pyspark.shell import spark
from pyspark.sql import SQLContext
from utils.CaricoManager import *
import argparse
from utils.Costants import PARQUET_FILE_CARGO, PARQUET_FILE_PRENOTATION


if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    parser = argparse.ArgumentParser(description='Visualization of statistics')
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
        plotCaricoPerNaveTotPrenotation(dataframe, dataframe_max_mq)




