from pyspark.shell import spark
from pyspark.sql import SQLContext
from matplotlib import pyplot as plt
from SQLManager import SQLManager


if __name__ == "__main__":
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    #df = sqlContext.read.parquet('hdfs://localhost:9000/tesi_siremar/capienza_garage.parquet').toPandas()
    sql = "SELECT tab_metri_garage_navi.*,ship_name FROM tab_metri_garage_navi INNER JOIN tab_ship on tab_metri_garage_navi.ship_id = tab_ship.ship_id order by ship_id"
    df = SQLManager.getInstance().execute_query(string_sql=sql)

    res = df.plot.bar(x="ship_name", y=["metri_garage_navi_spazio_totale", "metri_garage_navi_spazio_s18"],
                      figsize=(22, 10))
    plt.grid()
    res.legend(["Capienza Totale(mq)", "Capienza S18(mq)"])
    plt.show()