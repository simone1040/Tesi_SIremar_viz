from pyspark.shell import spark
from pyspark.sql import SQLContext
from utils.CaricoManager import *


if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    dataframe = getMaxCaricoNave()
    if not dataframe.empty:
        plotMaxCaricoNave(dataframe)




