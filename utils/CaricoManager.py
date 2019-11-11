from utils.SQLManager import SQLManager
from matplotlib import pyplot as plt
from utils.Costants import ASSETS
import pandas as pd

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
                    "WHERE `category_collection_va_rfid_code` = '{$category_collection_va_rfid_code}'"
            rfid_va_code = SQLManager.get_istance().execute_query(string_sql=query)
            if rfid_va_code.count() > 0:
                name = rfid_va_code.first().getString(0)
                lunghezza = rfid_va_code.first().getDouble(1)
                larghezza = rfid_va_code.first().getDouble(2)
                delta = rfid_va_code.first().getDouble(3)
                mq_occupati = (lunghezza * larghezza) + delta
        else:
            name = rfid_code.first().getString(0)
    return (name, mq_occupati)

def get_va_rfid_code_collection():
    query = "SELECT category_collection_va_rfid_code,category_collection_va_rfid_name,category_collection_va_rfid_lunghezza,category_collection_va_rfid_larghezza,category_collection_va_rfid_delta_larghezza " \
            "FROM `tab_category_collection_va_rfid` "
    return SQLManager.get_istance().execute_query(string_sql=query)


def compute_category_name_and_mq_occupati(dataframe):
    dataframe["mq_occupati"] = dataframe["category_collection_va_rfid_lunghezza"] * dataframe["category_collection_va_rfid_larghezza"] * dataframe["collection_quantity"].astype(str).astype(int) + dataframe["category_collection_va_rfid_delta_larghezza"]
    return dataframe


def compute_mq_occupati_dataframe(dataframe, dataframe_quantity, dataframe_veicoli):
    joined_dataframe = pd.merge(dataframe, dataframe_quantity, how="inner",
                                left_on=['tot_boardingcard_web_route_code'],
                                right_on=['tot_boardingcard_web_route_code'])
    print("numero righe dataframe con categorie essere umani --> ", joined_dataframe.shape[0])
    joined_dataframe = pd.merge(joined_dataframe, dataframe_veicoli, how="inner",
                                left_on="tot_boardingcard_web_detail_collection_rfid_code",
                                right_on="category_collection_va_rfid_code")
    print("numero righe dataframe filtrate per solo veicoli --> ", joined_dataframe.shape[0])
    final_dataframe = compute_category_name_and_mq_occupati(joined_dataframe)
    final_dataframe = final_dataframe.groupby(["tot_boardingcard_web_route_code", "route_cappelli_ship_code","route_cappelli_departure_timestamp"])[
        "mq_occupati"].agg("sum").reset_index(name ='tot_mq_occupati')
    print("numero righe mq occupati, comprendenti quelli che occupano 0 --> ", final_dataframe.shape[0])
    final_dataframe = final_dataframe[final_dataframe["tot_mq_occupati"] > 0]
    print("numero righe mq occupati filtrate da quelle che occupano  0 --> ", final_dataframe.shape[0])
    return final_dataframe
