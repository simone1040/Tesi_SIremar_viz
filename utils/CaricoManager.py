from utils.SQLManager import SQLManager
from matplotlib import pyplot as plt

def getMaxCaricoNave():
    sql = "SELECT tab_metri_garage_navi.*,ship_name " \
          "FROM tab_metri_garage_navi " \
          "INNER JOIN tab_ship on tab_metri_garage_navi.ship_id = tab_ship.ship_id " \
          "order by ship_id"
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def plotMaxCaricoNave(dataframe):
    res = dataframe.plot.bar(x="ship_name", y=["metri_garage_navi_spazio_totale", "metri_garage_navi_spazio_s18"],
                      figsize=(22, 10))
    for p in res.patches:
        res.annotate(str(p.get_height()), (p.get_x(), p.get_height() * 1.010))
    plt.grid()
    plt.xlabel('Navi')
    plt.ylabel('Capienza garage in mq')
    res.legend(["Capienza Totale(mq)", "Capienza S18(mq)"])
    plt.savefig("./assets/max_carico.png")
    plt.show()