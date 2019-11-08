from pyspark.shell import spark
from pyspark.sql import SQLContext
from utils.CaricoManager import *
import argparse
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
        dataframe = sqlContext.read.parquet(PARQUET_FILE)
        dataframe_quantity = sqlContext.read.parquet(QUANTITY_PARQUET_FILE)
        joined_dataframe = dataframe.join(dataframe_quantity,
                                          "tot_boardingcard_web_route_code", "inner")
        final_dataframe = compute_category_name_and_mq_occupati(joined_dataframe)



