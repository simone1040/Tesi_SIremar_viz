from utils.SQLManager import SQLManager
from matplotlib import pyplot as plt
from utils.Costants import ASSETS

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
    plt.savefig(ASSETS + "max_carico.png")
    plt.show()


def get_info_from_rfid_code(category_collection_va_rfid_code):
    name = "Non Disponibile"
    mq_occupati = 0
    if category_collection_va_rfid_code > 0:
        query = "SELECT category_collection_rfid_name " \
                    "FROM `tab_category_collection_rfid` " \
                    "WHERE `category_collection_rfid_code` = '${category_collection_va_rfid_code}'"
        rfid_code = SQLManager.get_istance().execute_query(string_sql=query)
        if rfid_code.count() == 0:
            query = "SELECT category_collection_va_rfid_name,category_collection_va_rfid_lunghezza,category_collection_va_rfid_larghezza,category_collection_va_rfid_delta_larghezza " \
                    "FROM `tab_category_collection_va_rfid` " \
                    "WHERE `category_collection_va_rfid_code` = '${category_collection_va_rfid_code}'"
            rfid_va_code = SQLManager.get_istance().execute_query(string_sql=query)
            if(rfid_va_code.count() > 0):
                name = rfid_va_code.first().getString(0)
                lunghezza  = rfid_va_code.first().getDouble(1)
                larghezza  = rfid_va_code.first().getDouble(2)
                delta  = rfid_va_code.first().getDouble(3)
                mq_occupati = (lunghezza * larghezza) + delta
        else:
            name = rfid_code.first().getString(0)
    return (name, mq_occupati)

def compute_category_name_and_mq_occupati(dataframe):
    for index, row in dataframe.iterrows():
        print(row)