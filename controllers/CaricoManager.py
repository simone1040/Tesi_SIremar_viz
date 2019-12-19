from models.CaricoModel import *
from matplotlib import pyplot as plt
from utils.Costants import *
import pandas as pd


def compute_dataframe_from_route_cappelli(dataframe_route_cappelli,filter_dataframe):
    final_dataframe = pd.DataFrame(columns=["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
                 "metri_garage_navi_spazio_totale","tot_mq_occupati"])
    for index, row in dataframe_route_cappelli.iterrows():
        if len(row["route_cappelli_next_route_code"].replace(" ", "")) == 0: #Caso in cui il viaggio è finale
            departure_data = filter_dataframe["booking_ticket_departure_timestamp"] == row["route_cappelli_departure_timestamp"]
            ship_code = filter_dataframe["ship_code"] == row["route_cappelli_ship_code"]
            row = filter_dataframe[departure_data & ship_code].groupby(
                ["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
                 "metri_garage_navi_spazio_totale"])["tot_mq_occupati"].sum().reset_index(name='tot_mq_occupati')
        else: #caso in cui non è viaggio finale
            #Prendo l'intero viaggio che ha per primo viaggio Row
            complete_trip = from_first_trip_get_all_lines(row)
            last_tot_mq_occupati = 0
            #TODO DA RIVEDERE PERCHÈ NON FUNZIONA
            for index, trip in complete_trip.iterrows():
                porto_partenza = filter_dataframe["departure_port_name"] == trip["route_cappelli_departure_port_code"]
                departure_data = filter_dataframe["booking_ticket_departure_timestamp"] == trip["route_cappelli_departure_timestamp"]
                ship_code = trip["route_cappelli_ship_code"] == filter_dataframe["ship_code"]
                row = filter_dataframe[departure_data & porto_partenza & ship_code].groupby(
                        ["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
                        "metri_garage_navi_spazio_totale"])["tot_mq_occupati"].sum().reset_index(name='tot_mq_occupati')
                if index != 0:
                    porto_arrivo = filter_dataframe["arrival_port_name"] == trip["route_cappelli_arrival_port_code"]
                    ship_code = trip["route_cappelli_ship_code"] == filter_dataframe["ship_code"]
                    trip_code = trip["route_cappelli_trip_code"] == filter_dataframe["ticket_trip_code"]
                    data_arrival = filter_dataframe["booking_ticket_departure_timestamp"] < trip["route_cappelli_departure_timestamp"]
                    row_scesi = filter_dataframe[porto_arrivo & ship_code & trip_code & data_arrival].groupby(
                        ["booking_ticket_departure_timestamp", "ship_code", "departure_port_name", "arrival_port_name",
                         "metri_garage_navi_spazio_totale"])["tot_mq_occupati"].sum().reset_index(
                        name='tot_mq_occupati')
                    row["tot_mq_occupati"] = row["tot_mq_occupati"] + last_tot_mq_occupati - row_scesi["tot_mq_occupati"]
                    last_tot_mq_occupati = row["tot_mq_occupati"]
        if not row.empty:
            final_dataframe = final_dataframe.append(row, ignore_index=True)
    return final_dataframe

#Metodo che prende dalla route cappelli l'intero viaggio partendo dal primo
def from_first_trip_get_all_lines(first_trip):
    next_route_code = first_trip["route_cappelli_next_route_code"]
    final_route_cappelli_dataframe = pd.DataFrame(
        columns=["route_cappelli_trip_code", "route_cappelli_departure_timestamp", "route_cappelli_route_code", "route_cappelli_next_route_code",
                 "route_cappelli_departure_port_code", "route_cappelli_arrival_port_code", "route_cappelli_ship_code"])
    #Appendo la prima riga che mi passano
    final_route_cappelli_dataframe = final_route_cappelli_dataframe.append(first_trip, ignore_index=True)
    while next_route_code != "":
        next_trip = get_trip_from_route_code(next_route_code)
        if not next_trip.empty:
            final_route_cappelli_dataframe = final_route_cappelli_dataframe.append(next_trip, ignore_index=True)
            next_route_code = next_trip["route_cappelli_next_route_code"].replace(" ", "")
        else:
            next_route_code = ""
    return final_route_cappelli_dataframe

def compute_dataframe_tot_mq_occupati():
    return pd.merge(DATAFRAME_APPLICATION["dataframe_prenotazioni"], DATAFRAME_APPLICATION["dataframe_max_mq_occupati"], how="inner",
                                left_on="ship_code",
                                right_on="ship_code")

#Funzione che viene chiamata quando si clicca il tasto di generazione del grafico, che viene salvato sull'assets
def image_statistics_filtered(filter):
    list_of_ship_name = []
    joined_dataframe = DATAFRAME_APPLICATION["dataframe_tot_mq_occupati"]
    #PRENDO IL DATABASE DELLE ROUTE CAPPELLI COSI DA POTER FORMARE IL NUOVO DATABASE DA CUI SI EFFETTUA IL PLOT
    dataframe_route_cappelli = get_distinct_first_trip(filter["booking_ticket_departure_timestamp"],
                                                       filter["booking_ticket_arrival_timestamp"])
    for key, values in filter.items():
        if values != "":
            if key == "ship":
                joined_dataframe = joined_dataframe[joined_dataframe["ship_code"].isin(filter["ship"])]
                #Filtro il dataframe route cappelli così da avere solo le navi interessate
                dataframe_route_cappelli = dataframe_route_cappelli[dataframe_route_cappelli["route_cappelli_ship_code"].isin(filter["ship"])]
            if key == "departure_port_code":
                port_name = from_port_code_get_name(filter["departure_port_code"])
                joined_dataframe = joined_dataframe[joined_dataframe["departure_port_name"] == port_name]
            if key == "arrival_port_code":
                port_name = from_port_code_get_name(filter["arrival_port_code"])
                joined_dataframe = joined_dataframe[joined_dataframe["arrival_port_name"] == port_name]
            if key == "booking_ticket_departure_timestamp":
                booking_ticket_departure_timestamp = filter["booking_ticket_departure_timestamp"]
                joined_dataframe = joined_dataframe[joined_dataframe["booking_ticket_departure_timestamp"] >= booking_ticket_departure_timestamp]
            if key == "booking_ticket_arrival_timestamp":
                booking_ticket_arrival_timestamp = filter["booking_ticket_arrival_timestamp"]
                joined_dataframe = joined_dataframe[joined_dataframe["booking_ticket_departure_timestamp"] <= booking_ticket_arrival_timestamp]

    dataframe_to_plot = compute_dataframe_from_route_cappelli(dataframe_route_cappelli, joined_dataframe)
    fig = plt.figure(figsize=(IMAGE_WIDTH/IMAGE_INFO["dpi_monitor"], IMAGE_HEIGHT/IMAGE_INFO["dpi_monitor"]), dpi=IMAGE_INFO["dpi_monitor"])

    for values in dataframe_to_plot.ship_code.unique():
        #INIZIO DATAFRAME PER IL LIMITE CHE COSI PRENDE L'INTERO GRAFICO
        dataframe_lim = pd.DataFrame(dataframe_to_plot.booking_ticket_departure_timestamp.unique(),columns =['booking_ticket_departure_timestamp'])
        dataframe_lim["metri_garage_navi_spazio_totale"] = dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["metri_garage_navi_spazio_totale"].iloc[0]
        #FINE

        #INIZIO PRENDO IL NOME DELLA NAVE E LO APPENDO DUE VOLTE PERCHE LO USO DUE VOLTE NEL PLOT
        ship_name = get_ship_name(values)
        list_of_ship_name.append(ship_name)
        list_of_ship_name.append(ship_name)
        #FINE

        #INIZIO PLOT DEL LIMITE E DEI PUNTI
        plt.plot(dataframe_lim["booking_ticket_departure_timestamp"],
                 dataframe_lim["metri_garage_navi_spazio_totale"],label=ship_name)

        plt.plot(dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["booking_ticket_departure_timestamp"],
             dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["tot_mq_occupati"], 'o',label=ship_name)
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



