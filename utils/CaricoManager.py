from utils.SQLManager import SQLManager
from matplotlib import pyplot as plt
from utils.Costants import *
import pandas as pd

def getMaxCaricoNave():
    sql = "SELECT tab_metri_garage_navi.*,ship_name,ship_code " \
          "FROM tab_metri_garage_navi " \
          "INNER JOIN tab_ship on tab_metri_garage_navi.ship_id = tab_ship.ship_id " \
          "order by ship_id"
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_distinct_tratte():
    sql = "SELECT booking_ticket_departure_port_code,booking_ticket_arrival_port_code " \
          "FROM tab_booking_ticket " \
          "GROUP BY booking_ticket_departure_port_code,booking_ticket_arrival_port_code "
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_distinct_ship():
    sql = "SELECT ship_code,ship_name " \
          "FROM tab_ship " \
          "ORDER BY ship_name"
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_ship_name(ship_code):
    sql = "SELECT ship_name " \
          "FROM tab_ship " \
          "WHERE ship_code='{}'" \
          "ORDER BY ship_code".format(ship_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    if not df.empty:
        return df["ship_name"].iloc[0]
    else:
        return ship_code

def from_port_code_get_name(port_code):
    sql = "SELECT port_name " \
          "FROM tab_port " \
          "WHERE port_code='{}' ".format(port_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    port_name = df["port_name"].iloc[0]
    return port_name

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

#Funzione che viene chiamata quando si clicca il tasto di generazione del grafico, che viene salvato sull'assets
def image_statistics_filtered(filter):
    list_of_ship_name = []
    joined_dataframe = pd.merge(DATAFRAME_APPLICATION["dataframe_prenotazioni"], DATAFRAME_APPLICATION["dataframe_max_mq_occupati"], how="inner",
                                left_on="ship_code",
                                right_on="ship_code")
    for key, values in filter.items():
        if values != "":
            if key == "ship":
                joined_dataframe = joined_dataframe[joined_dataframe["ship_code"].isin(filter["ship"])]
            if key == "departure_port_code":
                port_name = from_port_code_get_name(filter["departure_port_code"])
                joined_dataframe = joined_dataframe[joined_dataframe["departure_port_name"] == port_name]
            if key == "arrival_port_code":
                port_name = from_port_code_get_name(filter["arrival_port_code"])
                joined_dataframe = joined_dataframe[joined_dataframe["arrival_port_name"] == port_name]
            if key == "booking_ticket_departure_timestamp":
                booking_ticket_departure_timestamp = filter["booking_ticket_departure_timestamp"].toString("yyyy-MM-dd")
                joined_dataframe = joined_dataframe[joined_dataframe["booking_ticket_departure_timestamp"] >= booking_ticket_departure_timestamp]
            if key == "booking_ticket_arrival_timestamp":
                booking_ticket_arrival_timestamp = filter["booking_ticket_arrival_timestamp"].toString("yyyy-MM-dd")
                joined_dataframe = joined_dataframe[joined_dataframe["booking_ticket_departure_timestamp"] <= booking_ticket_arrival_timestamp]
    group_capienza_totale = joined_dataframe.groupby(
        ["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
         "metri_garage_navi_spazio_totale"])["tot_mq_occupati"]. \
        sum().reset_index(name='tot_mq_occupati')
    fig = plt.figure(figsize=(IMAGE_WIDTH/IMAGE_INFO["dpi_monitor"], IMAGE_HEIGHT/IMAGE_INFO["dpi_monitor"]), dpi=IMAGE_INFO["dpi_monitor"])

    for values in group_capienza_totale.ship_code.unique():
        #INIZIO DATAFRAME PER IL LIMITE CHE COSI PRENDE L'INTERO GRAFICO
        dataframe_lim = pd.DataFrame(group_capienza_totale.booking_ticket_departure_timestamp.unique(),columns =['booking_ticket_departure_timestamp'])
        dataframe_lim["metri_garage_navi_spazio_totale"] = group_capienza_totale[group_capienza_totale["ship_code"] == values]["metri_garage_navi_spazio_totale"].iloc[0]
        #FINE

        #INIZIO PRENDO IL NOME DELLA NAVE E LO APPENDO DUE VOLTE PERCHE LO USO DUE VOLTE NEL PLOT
        ship_name = get_ship_name(values)
        list_of_ship_name.append(ship_name)
        list_of_ship_name.append(ship_name)
        #FINE

        #INIZIO PLOT DEL LIMITE E DEI PUNTI
        plt.plot(dataframe_lim["booking_ticket_departure_timestamp"],
                 dataframe_lim["metri_garage_navi_spazio_totale"],label=ship_name)

        plt.plot(group_capienza_totale[group_capienza_totale["ship_code"] == values]["booking_ticket_departure_timestamp"],
             group_capienza_totale[group_capienza_totale["ship_code"] == values]["tot_mq_occupati"], 'o',label=ship_name)
        #FINE
    plt.title("Mq occupati da imbarchi dal " + booking_ticket_departure_timestamp + " al " + booking_ticket_arrival_timestamp, loc="center")
    plt.xlabel('Data di partenza')
    plt.legend()
    ax = fig.gca()  # get the current axis

    for i, p in enumerate(ax.get_lines()):  # this is the loop to change Labels and colors
        if p.get_label() in list_of_ship_name[:i]:  # check for Name already exists
            idx = list_of_ship_name.index(p.get_label())  # find ist index
            p.set_c(ax.get_lines()[idx].get_c())  # set color
            p.set_label('_' + p.get_label())  # hide label in auto-legend
    plt.legend()
    plt.xticks(rotation=45)
    plt.ylabel('Mq')
    plt.grid()
    return fig



