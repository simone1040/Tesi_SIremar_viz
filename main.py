from decimal import *

from pyspark.shell import spark
from pyspark.sql import SQLContext
from utils.CaricoManager import *
import argparse
import pandas as pd
from utils.Costants import PARQUET_FILE, QUANTITY_PARQUET_FILE


if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    parser = argparse.ArgumentParser(description='Visualization of statistics')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-gmc', help="Plot dei carichi max della nave e salvataggio sulla cartella assets", action='store_true')
    g.add_argument('-cat', help="Stampa della categoria e dello spazio occupato", action='store_true')
    args = parser.parse_args()

    if args.gmc:
        dataframe = getMaxCaricoNave()
        if not dataframe.empty:
            plotMaxCaricoNave(dataframe)

    if args.cat:
        print("CARICAMENTO DATAFRAME...\n")
        dataframe = sqlContext.read.parquet(PARQUET_FILE).toPandas()
        dataframe_veicoli = get_va_rfid_code_collection()
        dataframe_quantity = sqlContext.read.parquet(QUANTITY_PARQUET_FILE).toPandas()
        final_dataframe = compute_final_dataframe(dataframe=dataframe, dataframe_quantity=dataframe_quantity, dataframe_veicoli=dataframe_veicoli)
        print(final_dataframe.groupby(["tot_boardingcard_web_route_code","route_cappelli_ship_code"])["mq_occupati"].agg("sum"))



