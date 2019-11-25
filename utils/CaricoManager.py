from utils.SQLManager import SQLManager
from matplotlib import pyplot as plt
from utils.Costants import ASSETS
import pandas as pd

def getMaxCaricoNave():
    sql = "SELECT tab_metri_garage_navi.*,ship_name,ship_code " \
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


def plotCaricoPerNave(dataframe,dataframe_max_mq):
    joined_dataframe = pd.merge(dataframe, dataframe_max_mq, how="inner",
                                left_on="route_cappelli_ship_code",
                                right_on="ship_code")
    for ship_code, group in joined_dataframe.groupby(joined_dataframe.ship_code):
        ship_name = group["ship_name"].iloc[0]
        fig, (ax1, ax2) = plt.subplots(2)

        ax1.plot(group["route_cappelli_departure_timestamp"], group["metri_garage_navi_spazio_totale"])
        ax1.plot(group[group["category_collection_va_rfid_s18"] == 0]["route_cappelli_departure_timestamp"], group[group["category_collection_va_rfid_s18"] == 0]["tot_mq_occupati"],'o')
        ax1.legend(["Capienza Totale < S18(mq)", "Occupati < S18(mq)"])
        ax1.set_title("Mq occupati imbarchi 2018-2019 da nave " + ship_name, loc="center")
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel('Data di partenza')
        ax1.set_ylabel('Mq')
        ax1.grid()

        ax2.plot(group["route_cappelli_departure_timestamp"], group["metri_garage_navi_spazio_s18"])
        ax2.plot(group[group["category_collection_va_rfid_s18"] == 1]["route_cappelli_departure_timestamp"], group[group["category_collection_va_rfid_s18"] == 1]["tot_mq_occupati"],'o')
        ax2.legend(["Capienza Totale S18(mq)", "Occupati > S18(mq)"])
        ax2.tick_params(labelrotation=90)
        ax2.set_xlabel('Data di partenza')
        ax2.set_ylabel('Mq')
        ax2.grid()
        plt.savefig(ASSETS + "divided_carico/divided_carico_"+ship_code+".png")
    plt.show()


def plotCaricoPerNavePrenotazioni(dataframe,dataframe_max_mq):
    joined_dataframe = pd.merge(dataframe, dataframe_max_mq, how="inner",
                                left_on="ship_code",
                                right_on="ship_code")
    for ship_code, group in joined_dataframe.groupby(joined_dataframe.ship_code):
        ship_name = group["ship_name"].iloc[0]
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.plot(group["booking_ticket_departure_timestamp"], group["metri_garage_navi_spazio_totale"])
        ax1.plot(group[group["boardingcard_category_s18"] == 0]["booking_ticket_departure_timestamp"], group[group["boardingcard_category_s18"] == 0]["tot_mq_occupati"], 'o')
        ax1.legend(["Capienza Totale < S18(mq)", "Occupati < S18(mq)"])
        ax1.set_title("Mq occupati imbarchi 2018-2019 da nave " + ship_name, loc="center")
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel('Data di partenza')
        ax1.set_ylabel('Mq')
        ax1.grid()

        ax2.plot(group["booking_ticket_departure_timestamp"], group["metri_garage_navi_spazio_s18"])
        ax2.plot(group[group["boardingcard_category_s18"] == 1]["booking_ticket_departure_timestamp"], group[group["boardingcard_category_s18"] == 1]["tot_mq_occupati"],'o')
        ax2.legend(["Capienza Totale S18(mq)", "Occupati > S18(mq)"])
        ax2.tick_params(labelrotation=90)
        ax2.set_xlabel('Data di partenza')
        ax2.set_ylabel('Mq')
        ax2.grid()
        plt.savefig(ASSETS + "divided_carico_prenotation/divided_carico_"+ship_code+".png")
    plt.show()

def plotCaricoPerNaveTot(dataframe, dataframe_max_mq):
    joined_dataframe = pd.merge(dataframe, dataframe_max_mq, how="inner",
                                left_on="route_cappelli_ship_code",
                                right_on="ship_code")
    for ship_code, group in joined_dataframe.groupby(joined_dataframe.ship_code):
        ship_name = group["ship_name"].iloc[0]
        group_capienza_totale = group.groupby(
            ["tot_boardingcard_web_route_code", "route_cappelli_ship_code", "route_cappelli_departure_timestamp",
             "metri_garage_navi_spazio_totale"])["tot_mq_occupati"]. \
            sum().reset_index(name='tot_mq_occupati')
        plt.figure()
        plt.plot(group_capienza_totale["route_cappelli_departure_timestamp"], group_capienza_totale["metri_garage_navi_spazio_totale"])
        plt.plot(group_capienza_totale["route_cappelli_departure_timestamp"], group_capienza_totale["tot_mq_occupati"], 'o')
        plt.title("Mq occupati da imbarchi 2018-2019 da nave " + ship_name, loc="center")
        plt.legend(["Capienza Totale(mq)", "Occupati(mq)"])
        plt.xlabel('Data di partenza')
        plt.ylabel('Mq')
        plt.grid()
        plt.savefig(ASSETS + "tot_carico/tot_carico_" + ship_code + ".png")
    plt.show()

def plotCaricoPerNaveTotPrenotation(dataframe, dataframe_max_mq):
    joined_dataframe = pd.merge(dataframe, dataframe_max_mq, how="inner",
                                left_on="ship_code",
                                right_on="ship_code")
    for ship_code, group in joined_dataframe.groupby(joined_dataframe.ship_code):
        ship_name = group["ship_name"].iloc[0]
        group_capienza_totale = group.groupby(
            ["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
             "metri_garage_navi_spazio_totale"])["tot_mq_occupati"]. \
            sum().reset_index(name='tot_mq_occupati')
        plt.figure()
        plt.plot(group_capienza_totale["booking_ticket_departure_timestamp"], group_capienza_totale["metri_garage_navi_spazio_totale"])
        plt.plot(group_capienza_totale["booking_ticket_departure_timestamp"], group_capienza_totale["tot_mq_occupati"], 'o')
        plt.title("Mq occupati da imbarchi 2018-2019 da nave " + ship_name, loc="center")
        plt.legend(["Capienza Totale(mq)", "Occupati(mq)"])
        plt.xlabel('Data di partenza')
        plt.ylabel('Mq')
        plt.grid()
        plt.savefig(ASSETS + "tot_carico_prenotation/tot_carico_" + ship_code + ".png")
    plt.show()
