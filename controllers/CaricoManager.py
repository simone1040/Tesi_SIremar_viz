from models.CaricoModel import *
from matplotlib import pyplot as plt
from utils.Costants import *
from utils.MyLogger import writeLog
import pandas as pd


def get_filtered_dataframe(dataframe, filter):
    for key, values in filter.items():
        if values != "":
            if key == "ship":
                writeLog(levelLog.INFO,"CaricoManager","Sto filtrando per le seguenti navi --> {}".format(filter["ship"]))
                dataframe = dataframe[dataframe["ship_code"].isin(filter["ship"])]
            if key == "departure_port_code":
                port_name = from_port_code_get_name(filter["departure_port_code"])
                dataframe = dataframe[dataframe["departure_port_name"] == port_name]
            if key == "arrival_port_code":
                port_name = from_port_code_get_name(filter["arrival_port_code"])
                dataframe = dataframe[dataframe["arrival_port_name"] == port_name]
            if key == "booking_ticket_departure_timestamp":
                booking_ticket_departure_timestamp = filter["booking_ticket_departure_timestamp"]
                dataframe = dataframe[dataframe["booking_ticket_departure_timestamp"] >= booking_ticket_departure_timestamp]
            if key == "booking_ticket_arrival_timestamp":
                booking_ticket_arrival_timestamp = filter["booking_ticket_arrival_timestamp"]
                dataframe = dataframe[dataframe["booking_ticket_departure_timestamp"] <= booking_ticket_arrival_timestamp]
    return dataframe

#Funzione che dalla data, mi da una rapprentazione che non tiene conto dell'anno
def get_month_day_from_date(data):
    splitted_data = data.split("-")
    return splitted_data[1] + "-" + splitted_data[2]

def get_year_from_date(data):
    return data.split("-")[0]

#Funzione che aggiunge la colonna departure timestamp da DAta-ora in mese-giorno
def transform_departure_timestamp(dataframe_to_plot, ship_filter):
    dataframe_to_plot["booking_ticket_departure_timestamp"] = dataframe_to_plot[
        "booking_ticket_departure_timestamp"].apply(lambda x: x.split(" ")[0])
    if not ship_filter:
        dataframe_to_plot["departure_month_day"] = dataframe_to_plot["booking_ticket_departure_timestamp"]\
        .apply(lambda x: get_month_day_from_date(x))
        dataframe_to_plot["year"] = dataframe_to_plot["booking_ticket_departure_timestamp"].apply(
            lambda x: get_year_from_date(x))
        # Ordino le righe per la nuova colonna
        dataframe_to_plot = dataframe_to_plot.sort_values(by=["departure_month_day"])
    else:
        # Ordino le righe per il departure timestamp
        dataframe_to_plot = dataframe_to_plot.sort_values(by=["booking_ticket_departure_timestamp"])

    return dataframe_to_plot

def build_image_to_show(dataframe_to_plot, filter):
    fig = plt.figure(figsize=(IMAGE_WIDTH / IMAGE_INFO["dpi_monitor"], IMAGE_HEIGHT / IMAGE_INFO["dpi_monitor"]),
                     dpi=IMAGE_INFO["dpi_monitor"])
    #TRASFORMO IL DATAFRAME IN BASE AL CHECK DELL'UTILIZZO DELLE NAVE COME FILTRO
    dataframe_to_plot = transform_departure_timestamp(dataframe_to_plot, filter["year_graphics"])

    dataframe_mq_occupati = DATAFRAME_APPLICATION["dataframe_max_mq_occupati"]
    #INIZIALIZZO LA LISTA DELLE NAVI
    list_of_ship_name = []
    # PRENDO DAI FILTRI LA DATA DI PARTENZA E ARRIVO PER MOSTRARLA
    booking_ticket_arrival_timestamp = filter["booking_ticket_arrival_timestamp"]
    booking_ticket_departure_timestamp = filter["booking_ticket_departure_timestamp"]

    for values in dataframe_to_plot.ship_code.unique():
        #INIZIO DATAFRAME PER IL LIMITE CHE COSI PRENDE L'INTERO GRAFICO
        mq_max = dataframe_mq_occupati[dataframe_mq_occupati["ship_code"] == values][
            "metri_garage_navi_spazio_totale"].iloc[0]
        if filter["year_graphics"]:
            dataframe_lim = pd.DataFrame(dataframe_to_plot.booking_ticket_departure_timestamp.unique(),
                                     columns=['booking_ticket_departure_timestamp'])
            field_to_show = 'booking_ticket_departure_timestamp'
        else:
            dataframe_lim = pd.DataFrame(dataframe_to_plot.departure_month_day.unique(),
                                         columns=['departure_month_day'])
            field_to_show = 'departure_month_day'
        dataframe_lim["metri_garage_navi_spazio_totale"] = mq_max
        # FINE
        # INIZIO PRENDO IL NOME DELLA NAVE E LO APPENDO DUE VOLTE PERCHE LO USO DUE VOLTE NEL PLOT
        ship_name = get_ship_name(values)
        list_of_ship_name.append(ship_name)
        list_of_ship_name.append(ship_name)
        # FINE
        # INIZIO PLOT DEL LIMITE E DEI PUNTI
        plt.plot(dataframe_lim[field_to_show],
            dataframe_lim["metri_garage_navi_spazio_totale"], label=ship_name)
        #PLOT DEI DATI
        if filter["year_graphics"]:
            plt.plot(dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["booking_ticket_departure_timestamp"],
                dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["tot_mq_occupati"], 'o', label=ship_name)
        else:
            plt.plot(dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["departure_month_day"],
                     dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["tot_mq_occupati"], 'o',
                     label=ship_name)
        # FINE
    plt.title(
        "Mq occupati da imbarchi dal " + booking_ticket_departure_timestamp + " al " + booking_ticket_arrival_timestamp,
        loc="center")
    plt.xlabel('Data di partenza')
    plt.legend()
    return fig, list_of_ship_name

def get_labels_with_year(ax):
    current_month = -1
    labels = []
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        text = label.get_text()
        exploded_text = text.split("-")
        month = int(exploded_text[1].lstrip("0"))
        if current_month == -1:
            current_month = month
            labels.append(text)
        elif current_month < month:
            current_month = month
            labels.append(text)
        else:
            if ((current_month == 12) and (month == 1)):
                current_month = month
                labels.append(text)
    return labels

def get_label_without_year(ax):
    current_month = -1
    labels = []
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        text = label.get_text()
        exploded_text = text.split("-")
        month = int(exploded_text[0].lstrip("0"))
        if current_month == -1:
            current_month = month
            labels.append(text)
        elif current_month < month:
            current_month = month
            labels.append(text)
    return labels

def get_label_x_axis(ax, filter_ship):
    if filter_ship:
        labels = get_labels_with_year(ax)
    else:
        labels = get_label_without_year(ax)
    return labels


def set_fig_properties(labels):
    plt.legend()
    plt.xticks(labels, rotation=30)
    plt.ylabel('Mq')
    plt.grid()

def color_same_ship_with_same_color(ax, list_of_ship_name):
    for i, p in enumerate(ax.get_lines()):  # this is the loop to change Labels and colors
        if p.get_label() in list_of_ship_name[:i]:  # check for Name already exists
            idx = list_of_ship_name.index(p.get_label())  # find ist index
            p.set_c(ax.get_lines()[idx].get_c())  # set color
            p.set_label('_' + p.get_label())  # hide label in auto-legend

#Funzione che viene chiamata quando si clicca il tasto di generazione del grafico, che viene salvato sull'assets
def image_statistics_filtered(filter):
    # PRENDO IL DATABASE DELLE PRENOTAZIONI
    dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
    #EFFETTUO IL FILTRAGGIO PER I FILTRI SELEZIONATI
    dataframe_to_plot = get_filtered_dataframe(dataframe_to_plot, filter)

    if not dataframe_to_plot.empty:
        fig, list_of_ship_name = build_image_to_show(dataframe_to_plot, filter)
        ax = fig.gca()  # get the current axis
        color_same_ship_with_same_color(ax, list_of_ship_name)
        fig.canvas.draw()
        labels = get_label_x_axis(ax, filter["year_graphics"])
        set_fig_properties(labels)
        return fig
    else:
        return None



